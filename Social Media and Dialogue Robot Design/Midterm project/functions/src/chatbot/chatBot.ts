import * as functions from 'firebase-functions'
import { WebhookEvent, EventMessage, validateSignature } from "@line/bot-sdk"
import * as dialogflow from '../dialogflow/dialogflow'
import { LINE } from "./chatBotConfig"
import { DialogMessage } from '../chatbot/viewModel'


export const lineWebhook = functions.https.onRequest((req, res) => {
  const signature = req.headers["x-line-signature"] as string
  if (validateSignature(JSON.stringify(req.body), LINE.channelSecret, signature)) {
    const events = req.body.events as Array<WebhookEvent>
    for (const event of events)
      eventDispatcher(event)
  }
  res.status(200).send("OK")
})

const eventDispatcher = (event: WebhookEvent): void => {
  const lineId = event.source.userId as string
  console.log("lineId :", lineId)

  let dialogMessage = {} as DialogMessage
  dialogMessage.lineId = lineId
  dialogMessage.parameters = {
    time: event.timestamp
  }
  
  switch (event.type) {
    case "follow":
      dialogMessage.event = "follow"
      dialogflow.dialogflowAgent(dialogMessage)
      break;

    case "message":
      const message = event.message as EventMessage
      messageDispatcher(message, dialogMessage)
      break

    default:
      break
  }
}

const messageDispatcher = (message: EventMessage, dialogMessage: DialogMessage): void => {
  switch (message.type) {
    case "text":
      console.log(message.text)
      dialogMessage.userMessage = message.text
      break

    case "location":
      dialogMessage.event = "location"
      dialogMessage.parameters.lat = message.latitude
      dialogMessage.parameters.lon = message.longitude
      break

    case "image":
      dialogMessage.event = "image"
      dialogMessage.userMessage = "checkInImageType"
      dialogMessage.parameters.messageId = message.id
      break

    case "sticker":
    case "file":
    case "audio":
    case "video":
      dialogMessage.event = "image"
      dialogMessage.userMessage = "checkInImageErrorType"
      dialogMessage.parameters.messageId = message.id
      break

    default:
      break
  }
  console.log(dialogMessage)
  dialogflow.dialogflowAgent(dialogMessage)
}