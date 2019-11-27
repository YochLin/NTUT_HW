import * as dialogflow from 'dialogflow'
import * as structjson from './structJson'
import * as workflow from '../actionService/workFlow'
import * as lineService from '../chatbot/lineService'
import { DialogMessage } from '../chatbot/viewModel'

const dialogflowConfig = {
  path: "src/dialogflow/serviceAccountKey.json",
  projectId: "hospitallinechat",
  languageCode: 'zh-HK'
}

let sessionClient: any

export const dialogflowAgent = async (dialogMessage: DialogMessage) => {

  const sessionId = dialogMessage.lineId
  sessionClient = new dialogflow.SessionsClient({ keyFilename: dialogflowConfig.path });
  const sessionPath = sessionClient.sessionPath(dialogflowConfig.projectId, sessionId)

  let queryInput: any

  if (dialogMessage.userMessage) {
    queryInput = {
      text: {
        text: dialogMessage.userMessage,
        languageCode: dialogflowConfig.languageCode
      }
    }
  }

  if (dialogMessage.event) {
    console.log("event :", dialogMessage.event)
    queryInput = {
      event: {
        name: dialogMessage.event,
        languageCode: dialogflowConfig.languageCode,
        parameters: structjson.jsonToStructProto(dialogMessage.parameters)
      }
    }
  }

  const request = {
    session: sessionPath,
    queryInput: queryInput
  }

  await sessionClient.detectIntent(request).then(async (responses) => {
    const result = responses[0].queryResult

    if (result.fulfillmentMessages) {
      const fulfillmentMessages = result.fulfillmentMessages
      for (const fulfillmentMessage of fulfillmentMessages) {
        let responseMessage = fulfillmentMessage.text.text[0].replace(/\\n/g, '\n')
        if (responseMessage) {
          dialogMessage.resultMessage = responseMessage
          await lineService.pushMessage(dialogMessage)
        }
      }
    }

    if (result.action) {
      console.log("action:", result.action)
      dialogMessage.action = result.action

      const parameters = structjson.structProtoToJson(result.parameters) as any
      dialogMessage.parameters = Object.assign(dialogMessage.parameters, parameters)
      actionDispatcher(dialogMessage)
    }

  }).catch(err => console.log(err));
}

export const actionDispatcher = (dialogMessage: DialogMessage): void => {
  const action = dialogMessage.action

  switch (action) {
    case "follow":
      workflow.follow(dialogMessage)
      break;

    case "bind-bindMember":
      workflow.bind(dialogMessage)
      break;
      
    case "report":
      workflow.reportRecords(dialogMessage)
      break;  
    
    case "registerInTime":
      workflow.registerInTime(dialogMessage)
      break;
    
    case "registerDepartment":
      workflow.registerDepartment(dialogMessage)
      break;
    
    case "checkInLocation":
      workflow.checkInLocation(dialogMessage)
      break;
    
    case "getOpenHours":
      workflow.getOpenHours(dialogMessage)
      break;
    
    case "bindNewMemberID":
      workflow.bindNewMemberID(dialogMessage)
      break;

    case "bindNewMemberIformation":
      workflow.bindNewMemberIformation(dialogMessage)
      break;

    case "diseaseName":
      workflow.diseaseKnowledge(dialogMessage)
      break;

    case "showReport":
      workflow.showReport(dialogMessage)
      break;

    case "getMemberData":
      workflow.getMemberData(dialogMessage)
      break;

    case "setMemberRole":
      workflow.setMemberRole(dialogMessage)
      break;

    default:
      break;
  }
}
