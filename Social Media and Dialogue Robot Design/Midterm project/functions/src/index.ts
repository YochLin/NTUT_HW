import * as functions from 'firebase-functions'
import * as firebaseAdmin from "firebase-admin"
firebaseAdmin.initializeApp(functions.config().firebase)

import * as chatbot from "./chatbot/chatBot"
import * as firestore from"./firestore/databaseService"

export const lineWebhook = chatbot.lineWebhook 
export const databaseServcie = firestore.databaseService

