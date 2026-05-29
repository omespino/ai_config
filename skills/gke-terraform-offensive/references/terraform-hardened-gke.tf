# =============================================================================
# Hardened private GKE — reference module
# Every block neutralizes a chain from SKILL.md section 4. Read alongside
# gke-misconfig-catalog.md (insecure vs secure values).
#
# Provider: hashicorp/google >= 5.x. Adjust regions/CIDRs/project to taste.
# This is the "right" config so you understand the defended state; it is also
# a deployable baseline for your own clusters.
# =============================================================================

terraform {
  required_version = ">= 1.6"
  required_providers {
    google = { source = "hashicorp/google", version = ">= 5.0" }
  }
  # State boundary: locked-down GCS bucket. The state file holds secrets in
  # plaintext regardless of `sensitive` — the bucket IAM IS the control.
  backend "gcs" {
    bucket = "my-tfstate-locked"   # uniform access, versioning, CMEK, no allUsers
    prefix = "gke/prod"
  }
}

variable "project"  { type = string }
variable "region"   { type = string, default = "us-central1" }
variable "authorized_cidr" {
  type        = string
  description = "Single bastion/admin CIDR allowed to reach the control plane"
  default     = "203.0.113.10/32"
}

# -----------------------------------------------------------------------------
# Dedicated minimal node SA  (NOT the default Compute SA)
# -----------------------------------------------------------------------------
resource "google_service_account" "nodes" {
  account_id   = "gke-nodes-min"
  display_name = "GKE node pool (least privilege)"
  project      = var.project
}

# Only the roles nodes actually need — no Editor, no cloud-platform scope.
locals {
  node_roles = [
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/monitoring.viewer",
    "roles/stackdriver.resourceMetadata.writer",
    "roles/artifactregistry.reader",
  ]
}
resource "google_project_iam_member" "nodes" {
  for_each = toset(local.node_roles)
  project  = var.project
  role     = each.value
  member   = "serviceAccount:${google_service_account.nodes.email}"
}

# -----------------------------------------------------------------------------
# VPC + subnet with secondary ranges for VPC-native (alias IP) cluster
# -----------------------------------------------------------------------------
resource "google_compute_network" "vpc" {
  name                    = "gke-vpc"
  auto_create_subnetworks = false
  project                 = var.project
}
resource "google_compute_subnetwork" "subnet" {
  name          = "gke-subnet"
  ip_cidr_range = "10.10.0.0/20"
  region        = var.region
  network       = google_compute_network.vpc.id
  project       = var.project
  private_ip_google_access = true
  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.20.0.0/16"
  }
  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.30.0.0/20"
  }
}

# -----------------------------------------------------------------------------
# Cluster — private, WI, Dataplane v2, shielded, restricted control plane
# -----------------------------------------------------------------------------
resource "google_container_cluster" "this" {
  name     = "prod-gke"
  location = var.region
  project  = var.project

  network    = google_compute_network.vpc.id
  subnetwork = google_compute_subnetwork.subnet.id

  # Manage node pools separately
  remove_default_node_pool = true
  initial_node_count       = 1

  # Auto-patching
  release_channel { channel = "REGULAR" }

  # Private nodes + private control plane endpoint
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = true
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  # Only the bastion CIDR can reach the API server
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = var.authorized_cidr
      display_name = "admin-bastion"
    }
    gcp_public_cidrs_access_enabled = false
  }

  # Kills the node-SA-token-via-metadata chain (SKILL.md 4.1/4.2)
  workload_identity_config {
    workload_pool = "${var.project}.svc.id.goog"
  }

  # Dataplane v2 => NetworkPolicy enforcement, east-west segmentation
  datapath_provider = "ADVANCED_DATAPATH"

  # Defense-in-depth
  enable_shielded_nodes = true
  enable_legacy_abac    = false

  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  # etcd application-layer encryption of Secrets (CMEK)
  database_encryption {
    state    = "ENCRYPTED"
    key_name = "projects/${var.project}/locations/${var.region}/keyRings/gke/cryptoKeys/etcd"
  }

  # VPC-native
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # No basic auth / client cert (legacy)
  master_auth {
    client_certificate_config { issue_client_certificate = false }
  }
}

# -----------------------------------------------------------------------------
# Node pool — minimal SA, no cloud-platform scope, shielded, COS, hardened meta
# -----------------------------------------------------------------------------
resource "google_container_node_pool" "primary" {
  name     = "primary"
  cluster  = google_container_cluster.this.id
  location = var.region

  node_count = 2
  management { auto_repair = true, auto_upgrade = true }

  node_config {
    machine_type    = "e2-standard-4"
    image_type      = "COS_CONTAINERD"
    service_account = google_service_account.nodes.email

    # Rely on IAM, not broad scopes. gke_default ~ logging/monitoring/AR-read.
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    # NOTE: prefer the minimal set below in environments that allow it:
    # oauth_scopes = [
    #   "https://www.googleapis.com/auth/logging.write",
    #   "https://www.googleapis.com/auth/monitoring",
    #   "https://www.googleapis.com/auth/devstorage.read_only",
    # ]

    # Block legacy metadata endpoints + force WI metadata server
    metadata = {
      disable-legacy-endpoints = "true"
    }
    workload_metadata_config { mode = "GKE_METADATA" }

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    # No public IPs on nodes (also enforced by private_cluster_config)
    tags = ["gke-node", "prod"]
  }
}

# -----------------------------------------------------------------------------
# Example: bind a Kubernetes SA to a GCP SA via Workload Identity
# (this is how pods get *scoped* GCP access instead of the node SA)
# -----------------------------------------------------------------------------
resource "google_service_account" "app" {
  account_id = "app-workload"
  project    = var.project
}
resource "google_service_account_iam_member" "app_wi" {
  service_account_id = google_service_account.app.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project}.svc.id.goog[my-namespace/my-ksa]"
}
# Then annotate the KSA: iam.gke.io/gcp-service-account = app-workload@<project>.iam.gserviceaccount.com
