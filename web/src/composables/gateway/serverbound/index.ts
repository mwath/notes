import { IServerBound } from "./base";

type RequestJoinChannel = IServerBound<
  "request_join_channel",
  { page_id: number }
>;
type LeaveChannel = IServerBound<"leave_channel", {}>;
type Handshake = IServerBound<"handshake", { version: number }>;
type BlockModified = IServerBound<"block_modified", { block_id: string }>;
type BlockDeleted = IServerBound<"block_deleted", { block_id: string }>;
type BlockAdded = IServerBound<"block_added", { block_id: string }>;
type BlockMoved = IServerBound<
  "block_moved",
  { block_id: string; dest: number }
>;

export type ServerBound =
  | RequestJoinChannel
  | LeaveChannel
  | Handshake
  | BlockModified
  | BlockDeleted
  | BlockAdded
  | BlockMoved;
