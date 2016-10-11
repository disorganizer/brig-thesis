# Anhang: Protokolldefinitionen

## Internes Datenmodell von ``brig`` {#sec:data-model}

```c
syntax = "proto3";
package brig.store;
option go_package = "wire";

///////////// VERSION CONTROL STRUCTURES ///////////

message Author {
  string name = 1;
  string hash = 2;
}

// Optional merge information for merge commits
message Merge {
    string with = 1;
    bytes hash = 2;
}

message Checkpoint {
  // Link to the node id:
  uint64 id_link = 1;
  bytes hash = 2;
  uint64 index = 3;
  int32 change = 4;
  string author = 5;
}

// History is the history of a file:
message History {
    repeated Checkpoint hist = 1 [packed=false];
}

message CheckpointLink {
  uint64 id_link = 1;
  uint64 index = 2;
}

// Commits is an ordered list of commits
message Commits {
    repeated Commit commits = 1;
}

// Ref is a pointer to a single commit
message Ref {
    string name = 1;
    bytes hash = 2;
}

////////////// NODE BASICS /////////////

// Might be extended with more esoteric types in the future.
enum NodeType {
  UNKNOWN = 0;
  FILE = 1;
  DIRECTORY = 2;
  COMMIT = 3;
}

// An Object is a container for a file, a directory or a Ref.
message Node {
  // Type of this node (see above)
  NodeType type = 1;
  // Global identifier of this node, since hash and path
  // might change sometimes.
  uint64 ID = 2;

  // Size of the node in bytes:
  uint64 node_size = 3;

  // Timestamp formated as RFC 3339
  bytes mod_time = 4;

  // Hash of the node as multihash:
  bytes hash = 5;

  // Name of this node (i.e. path element)
  string name = 6;

  // Path must only be filled when exported to a client.
  // It may not be used internally and is not saved to the kv-store.
  string path = 7;

  // Individual types:
  File file = 8;
  Directory directory = 9;
  Commit commit = 10;
}

// Just a collection of nodes:
message Nodes {
  repeated Node nodes = 1;
}

////////////// CONCRETE NODES /////////////

message File {
  // Path to parent directory
  string parent = 1;

  // Key of this file:
  bytes key = 2;
}

message Directory {
  // Path to parent object:
  string parent = 1;

  // Directory contents (hashtable contents [name => link]):
  repeated bytes links = 2;
  repeated string names = 3;
}

// Commit is a bag of changes, either automatically done or by the user.
message Commit {
  // Hash of the parent commit:
  bytes parent = 1;

  // Commit message:
  string message = 2;

  // Author of this commit:
  Author author = 3;

  // Hash to the root tree:
  bytes root = 4;

  // List of checkpoints (one per file):
  repeated CheckpointLink changeset = 5;

  // Merge information if this is a merge commit.
  Merge merge = 6;

  // Checkpoints stored in the commit.
  // This is only used when exported to the client,
  // it is not stored in the kv-store.
  repeated Checkpoint checkpoints = 7;
}

//////////// EXPORT/IMPORT DATA //////////////

// Store is the exported form of a store.
message Store {
  // The boltdb format.
  bytes boltdb = 1;
}
```

## Protokoll zwischen zwei Knoten {#sec:rpc-proto}

```c
syntax = "proto3";
package brig.transfer;
option go_package = "wire";

import "store.proto";

enum RequestType {
    INVALID = 0;
    FETCH = 1;
    STORE_VERSION = 2;
    UPDATE_FILE = 3;
}

message Request {
	RequestType req_type = 1;
    int64 ID = 2;
    int64 nonce = 3;
}

message StoreVersionResponse {
    int32 version = 1;
}

message FetchResponse {
    brig.store.Store store = 1;
}

message Response {
	RequestType req_type = 1;
    int64 ID = 2;
    int64 nonce = 3;
    string error = 4;

    StoreVersionResponse store_version_resp = 5;
    FetchResponse fetch_resp = 6;
}
```
