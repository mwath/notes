import requests from "../requests";
import { APIResponse } from "../base";
import { Ref, ref } from "vue";
import { TokenModel } from "./login";

interface Code2FA {
  code: string;
}


