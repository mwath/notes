import { IServerBound } from "./base";

type RequestJoinChannel = IServerBound<
  "request_join_channel",
  { page_id: number }
>;
type LeaveChannel = IServerBound<"leave_channel", {}>;
type Handshake = IServerBound<"handshake", { version: number }>;

export type ServerBound = RequestJoinChannel | LeaveChannel | Handshake;
