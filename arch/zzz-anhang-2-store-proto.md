# Anhang: Protokolldefinitionen

## Internes Datenmodell von ``brig`` {#sec:data-model}

```c
package brig.store;
option go_package = "wire";

// Might be extended with more esoteric types in the future.
enum NodeType {
  UNKNOWN = 0;
  FILE = 1;
  DIRECTORY = 2;
  COMMIT = 3;
}

// An Object is a container for a file, a directory or a Ref.
message Node {
  required NodeType type = 1;

  // Individual types:
  optional File file = 2;
  optional Directory directory = 3;
  optional Commit commit = 4;
}

message File {
    required string path = 1;
    optional bytes key = 2;
    optional bytes hash = 3;
    required int64 file_size = 4;
    required int32 kind = 5;

    // Timestamp formated as RFC 3339
    required bytes mod_time = 6;
}

message Directory {
    required string name = 1;
    required uint64 file_size = 2;
    required bytes parent = 3;
    required bytes hash = 4;
    required bytes mod_time = 5;

    // Directory contents:
    repeated bytes links = 6;
    repeated string names = 7;
}

message Checkpoint {
    required bytes hash = 1;
    required bytes mod_time = 2;
    required int64 file_size = 3;
    required int32 change = 4;
    required string author = 5;
    required string path = 6;
    required string old_path = 7;
    required uint64 index = 8;
}

message History {
    repeated Checkpoint hist = 1 [packed=false];
}

// Optional merge information for merge commits
message Merge {
    required string with = 1;
    required bytes hash = 2;
}

// Commit is a bag of changes, either automatically done
// or by the user.
message Commit {
    required string message = 1;
    required string author = 2;
    required bytes mod_time = 3;
    required bytes hash = 4;
    required bytes tree_hash = 5;

    // List of checkpoints:
    repeated Checkpoint checkpoints = 6;

    // Link to parent hash (empty for initial commit):
    optional bytes parent_hash = 7;

    // Merge information if this is a merge commit.
    optional Merge merge = 8;
}

// Commits is an ordered list of commits
message Commits {
    repeated Commit commits = 1;
}

message Ref {
    required string name = 1;
    required bytes hash = 2;
    required int32 type = 3;
}
```

TODO: Bei änderung updaten

## Protokoll zwischen zwei Knoten {#sec:rpc-proto}

```c
package brig.transfer;
option go_package = "wire";

import "store.proto";

enum RequestType {
    INVALID = 0;
    FETCH = 1;
}

message Request {
	required RequestType req_type = 1;
    required int64 ID = 2;
    required int64 nonce = 3;
}

message StoreVersionResponse {
    required int32 version = 1;
}

message FetchResponse {
    required brig.store.Store store = 1;
}

message Response {
	required RequestType req_type = 1;
    required int64 ID = 2;
    required int64 nonce = 3;
    optional string error = 4;

    optional StoreVersionResponse store_version_resp = 5;
    optional FetchResponse fetch_resp = 6;
}
```

TODO: Bei änderung updaten
