import { Client, TextMessage, FlexMessage } from "@line/bot-sdk"
import { LINE } from "./chatBotConfig"
import { DialogMessage } from '../chatbot/viewModel'
import axios from "axios"
const qs = require('querystring');

export async function pushMessage(dialogMessage: DialogMessage) {
  const textMessage = {
    type: "text",
    text: dialogMessage.resultMessage
  } as TextMessage
  const accessToken = await getAccessToken()
  const lineClient = new Client({
    channelAccessToken: accessToken
  })
  return lineClient.pushMessage(dialogMessage.lineId, textMessage)
}

export async function getAccessToken(): Promise<string> {
  let accessToken
  const apiUrl = `https://api.line.me/v2/oauth/accessToken`
  const requestConfig = {
    headers: {
      "content-type": "application/x-www-form-urlencoded"
    }
  }
  const body = {
    "grant_type": "client_credentials",
    "client_id": LINE.channelId,
    "client_secret": LINE.channelSecret
  }

  return axios.post(apiUrl, qs.stringify(body), requestConfig).then(result => {
    accessToken = result.data.access_token
    console.log("Get LineAccessToken : ", accessToken)
    return accessToken
  }).catch(null)
}

export async function pushFlexMessage(dialogMessage: DialogMessage, contents: Array<any>){
  const carousel = {
    "type": "carousel",
    "contents": contents
  }
  const flexMessage = {
    type: "flex",
    altText: "查詢結果",
    contents: carousel
  } as FlexMessage

  const accessToken = await getAccessToken()
  const lineClient = new Client({
    channelAccessToken: accessToken
  })
  return lineClient.pushMessage(dialogMessage.lineId, flexMessage).catch(err => console.error(err))
}
