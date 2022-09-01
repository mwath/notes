import {
  ClientBound,
  ClientBoundMessages,
} from "@/composables/gateway/clientbound";
import { ServerBound } from "@/composables/gateway/serverbound";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useToast } from "vue-toastification";
import { usePageStore } from "./page";

type ClientBoundCallback<Key extends keyof ClientBoundMessages> = {
  (data: ClientBoundMessages[Key]): void;
};

export const useGatewayStore = defineStore("gateway", () => {
  const toast = useToast();
  const ws = ref<WebSocket>();
  const listeners: {
    [key in keyof ClientBoundMessages]?: ClientBoundCallback<key>[];
  } = {};
  let retry_time = 1;

  function connect() {
    const state = ws.value?.readyState;
    if (ws.value && (state == WebSocket.OPEN || state == WebSocket.CONNECTING))
      ws.value.close();

    ws.value = new WebSocket(GATEWAY_URL);
    ws.value.addEventListener("close", (ev) => {
      if (!ev.wasClean) {
        console.log("Reconnecting ...");
        setTimeout(connect, retry_time);
        retry_time = Math.min(retry_time * 2, 300);
      }
    });
    ws.value.addEventListener("open", () => {
      retry_time = 1;
      send({
        id: "handshake",
        data: { version: 0 },
      });
    });
    ws.value.addEventListener("message", (ev) => {
      const msg: ClientBound<keyof ClientBoundMessages> = JSON.parse(ev.data);
      const callbacks = listeners[msg.id];
      if (callbacks) for (const cb of callbacks) cb(msg.data as any);
    });
    ws.value.addEventListener("error", (ev) => {
      console.log("error", ev);
    });
  }

  function send(msg: ServerBound) {
    if (ws.value && ws.value.readyState == WebSocket.OPEN)
      ws.value.send(JSON.stringify(msg));
  }

  function on<Key extends keyof ClientBoundMessages>(
    eventName: Key,
    callback: ClientBoundCallback<Key>
  ) {
    if (listeners[eventName] === undefined) listeners[eventName] = [];
    listeners[eventName]?.push(callback);
  }

  on("login", (data) => {
    if (!data.success) {
      toast.error("Impossible de se connecter au serveur.");
    } else {
      const page_id = usePageStore().current?.id;
      if (page_id) send({ id: "request_join_channel", data: { page_id } });
    }
  });

  return {
    ws,
    connect,
    send,
    on,
  };
});
