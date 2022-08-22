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

export type ClientBoundMessages = {
  joined_channel: JoinedChannel;
  left_channel: LeftChannel;
  user_joined_channel: UserJoinedChannel;
  user_left_channel: UserLeftChannel;
  channel_not_found: ChannelNotFound;
  login: Login;
};

export interface ClientBound<Key extends keyof ClientBoundMessages> {
  id: Key;
  data: ClientBoundMessages[Key];
}
