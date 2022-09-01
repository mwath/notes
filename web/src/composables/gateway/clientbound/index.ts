import { Page } from "@/stores/page";

interface JoinedChannel {
  cid: number;
  page: Page;
}

interface LeftChannel {}

interface UserJoinedChannel {
  cid: number;
  uid: number;
  username: string;
}

interface UserLeftChannel {
  cid: number;
}

interface ChannelNotFound {
  page_id: number;
}

interface Login {
  success: boolean;
  version: number;
  username: string;
}

interface BlockModified {
  block_id: string;
}

interface BlockDeleted {
  block_id: string;
}

interface BlockAdded {
  block_id: string;
}

interface BlockMoved {
  block_id: string;
  dest: number;
}

export type ClientBoundMessages = {
  joined_channel: JoinedChannel;
  left_channel: LeftChannel;
  user_joined_channel: UserJoinedChannel;
  user_left_channel: UserLeftChannel;
  channel_not_found: ChannelNotFound;
  login: Login;
  block_modified: BlockModified;
  block_deleted: BlockDeleted;
  block_added: BlockAdded;
  block_moved: BlockMoved;
};

export interface ClientBound<Key extends keyof ClientBoundMessages> {
  id: Key;
  data: ClientBoundMessages[Key];
}
