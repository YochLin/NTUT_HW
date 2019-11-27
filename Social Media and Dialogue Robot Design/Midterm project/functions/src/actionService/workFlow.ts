import * as dialogflow from '../dialogflow/dialogflow'
import * as dataProxy from './dataProxy'
import { clinicId } from "../chatbot/chatBotConfig"
import { Member, Record, Clinic} from '../firestore/model'
import { DialogMessage } from '../chatbot/viewModel'
import * as lineService from '../chatbot/lineService'
import * as CheckTime from 'time-checker'
import * as databaseService from '../firestore/databaseService'
import { DiffieHellman } from 'crypto'

const timeChecker = new CheckTime({ timeZone: "Asia/Taipei" })

let members: Member
let records: Array<any>
let clinics: Clinic


const getModels = async (dialogMessage: DialogMessage) => {
  // 直接獲取下面所有內容
  clinics = await dataProxy.getClinicByClinicId(clinicId) as Clinic
  members = await dataProxy.getMemberByLineId(dialogMessage.lineId) as Member
  records = await dataProxy.getRecordsByMemberID(members.id) as Array<any>
}

export const follow = async (dialogMessage: DialogMessage) => {
  const lineId = dialogMessage.lineId
  const member = await dataProxy.getMemberByLineId(lineId)
  let event = "" as string
  if (member) {
    event = "follow-hasFollowed"
  } else {
    event = "bind-ask4Phone"
  }
  dialogMessage.event = event
  dialogflow.dialogflowAgent(dialogMessage)
}

export const bind = async (dialogMessage: DialogMessage) => {
  const lineId = dialogMessage.lineId
  const phone = dialogMessage.parameters.phone
  const member = await dataProxy.getMemberByPhone(phone)
  const clinic = await dataProxy.getClinicByClinicId(clinicId)

  let event = "" as string
  if (member) {
    if (member.lineId) {
      if (member.lineId == lineId) {
        event = "bind-hasBound"

      } else {
        event = "bind-phoneOccupied"
      }

    } else {
      event = "bind-bindSuccess"
      member.lineId = lineId
      databaseService.updateMember(member)
      dialogMessage.parameters = {
        name: member.name,
        clinicName: clinic.clinicName
      }
    }

  } else {
    event = "bind-phoneNotFound"
  }

  dialogMessage.event = event
  dialogMessage.parameters.lineId = lineId
  dialogMessage.parameters.phone = phone
  dialogflow.dialogflowAgent(dialogMessage)
}

export const showReport = async(dialogMessage: DialogMessage) =>{
  const event = "showReport"
  dialogMessage.event = event
  dialogflow.dialogflowAgent(dialogMessage)
}

const recordsFlexMessage = (records: Array<any>): any => {
  let contents = [] as Array<any>

  for(var i = 1; i < records.length; i ++){   // 第0筆為新用戶測試筆，所以跳過
    let record = records[i]
    contents.push(
      {
        "type": "bubble",
        "hero": {
          "type": "image",
          "url": "https://i.imgur.com/OtBh4YZ.png",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "cover",
          "action": {
            "type": "uri",
            "uri": "http://linecorp.com/"
          }
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": record.registerStore + "診所",
              "weight": "bold",
              "size": "xl"
            },
            {
              "type": "box",
              "layout": "vertical",
              "margin": "lg",
              "spacing": "sm",
              "contents": [
                {
                  "type": "box",
                  "layout": "baseline",
                  "spacing": "sm",
                  "contents": [
                    {
                      "type": "text",
                      "text": "日期",
                      "color": "#aaaaaa",
                      "size": "sm",
                      "flex": 1
                    },
                    {
                      "type": "text",
                      "text": record.registerDay,
                      "wrap": true,
                      "color": "#666666",
                      "size": "sm",
                      "flex": 5
                    }
                  ]
                },
                {
                  "type": "box",
                  "layout": "baseline",
                  "spacing": "sm",
                  "contents": [
                    {
                      "type": "text",
                      "text": "時間",
                      "color": "#aaaaaa",
                      "size": "sm",
                      "flex": 1
                    },
                    {
                      "type": "text",
                      "text": record.registerTime,
                      "wrap": true,
                      "color": "#666666",
                      "size": "sm",
                      "flex": 5
                    }
                  ]
                },
                          {
                  "type": "box",
                  "layout": "baseline",
                  "spacing": "sm",
                  "contents": [
                    {
                      "type": "text",
                      "text": "科別",
                      "color": "#aaaaaa",
                      "size": "sm",
                      "flex": 1
                    },
                    {
                      "type": "text",
                      "text": record.department,
                      "wrap": true,
                      "color": "#666666",
                      "size": "sm",
                      "flex": 5
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    )
  }
  return contents
}

export const reportRecords = async(dialogMessage: DialogMessage) =>{
  // 將目前月份的所有紀錄透過(flexMessage)給顯示出去
  await getModels(dialogMessage)
  const event = "showResult"
  let recordLen = await dataProxy.getRecordsLenght(members.id)
  const contents = recordsFlexMessage(records)
  
  dialogMessage.event = event
  dialogMessage.parameters = {
    name: members.name,
    recordsLen: recordLen 
  }
  lineService.pushFlexMessage(dialogMessage, contents)
  dialogflow.dialogflowAgent(dialogMessage)
}

export const registerInTime = async(dialogMessage: DialogMessage) =>{
    // 判斷目前時間是否為營業時間
  const lineId = dialogMessage.lineId
  const clinics =  await dataProxy.getClinicByClinicName(dialogMessage.parameters.clinic)
  const registerTime = dialogMessage.parameters.time
  const registerTimeState = verifyCheckInTime(registerTime, clinics)
  const member = await dataProxy.getMemberByLineId(lineId)
  console.log("CheckInTimeState:", registerTimeState)

  dialogMessage.parameters = {
    clinicName: clinics.clinicName,
    morningTime: clinics.openTime.morning,
    afternoonTime: clinics.openTime.afternoon,
    nightTime: clinics.openTime.night,
    departments: clinics.departments,
    registerTime: new Date(registerTime).toLocaleTimeString("zh-TW", {hour12: false, timeZone: 'Asia/Taipei'})
  }
  member.bufferMessage = clinics.clinicName

  let event = "" as string
  switch(registerTimeState){
    case 0:
      event = "registerTimeError"
      break;
    case 1:
    case 2:
    case 3:
      event = "registerTimeSuccess"
      break;

    default:
      break;
  }

  dialogMessage.event = event
  databaseService.updateMember(member)
  dialogflow.dialogflowAgent(dialogMessage)
}

const verifyCheckInTime = (checkInTime: number, clinic: Clinic): any => {
  if (!clinic) {
    return 0
  } else{
    if(timeChecker.byConditions(`${clinic.openTime.morning}`, checkInTime)) return 1
    else if(timeChecker.byConditions(`${clinic.openTime.afternoon}`, checkInTime)) return 2
    else if(timeChecker.byConditions(`${clinic.openTime.night}`, checkInTime)) return 3
    else return 0
  }
}

export const registerDepartment = async(dialogMessage: DialogMessage) =>{
  // 判斷輸入的科別是否與目前診所擁有的科別有誤
  console.log("registerDepartment", dialogMessage)
  const lineId = dialogMessage.lineId
  const today = new Date()
  const member = await dataProxy.getMemberByLineId(lineId)
  const records = {} as Record
  const clinics = await dataProxy.getClinicByClinicName(member.bufferMessage)
  const departments = clinics.departments 
  // 透過迴圈來判斷本診所內的所有科別是否與使用者所輸入的有誤
  for(let de of departments){
    if(de.department == dialogMessage.userMessage){
      de.numberSlip++
      dialogMessage.event = "registerSuccess"
      dialogMessage.parameters.numberSlip = de.numberSlip
      records.month =  `${today.getMonth() + 1}`
      records.registerDay = today.toLocaleDateString()
      records.registerTime = today.toLocaleTimeString()
      records.department = de.department
      records.registerStore = clinics.clinicName
      databaseService.setRecord(member, records)
    }
  }
  if(!dialogMessage.event){
    dialogMessage.event = "registerDepartmentError"
    dialogMessage.resultMessage = "本診所有提供以下科別提供掛號：\n"
    for(let de of departments){
      dialogMessage.resultMessage += 
      `${de.department}\n`
    }
    dialogMessage.resultMessage += "==================="
  }
  
  lineService.pushMessage(dialogMessage)   // 將錯誤動作時的文字推送出去
  databaseService.updateClinic(clinics.clinicId, clinics)    // 將有更新過後的 numberSlip 更新出去
  dialogflow.dialogflowAgent(dialogMessage)
}

export const checkInLocation = async(dialogMessage: DialogMessage) =>{
  // 確認目前位置與所有門診位置之間的距離
  let allClinic = await dataProxy.getClinics()   // 取得所有診所資訊
  let event = "checkInLocationSuccess"
  let countArray = 1  // 用來計數下面 contents 的長度順序
  const GPS = {
    lat: dialogMessage.parameters.lat,
    lon: dialogMessage.parameters.lon
  }
  const contents = [] as Array<any>
  // 透過得到的全部診所資訊與目前的位置做比對得到距離，在存到contents中
  for(let clinic of allClinic){
    const clinicLocation = {
      lat: clinic.clinicLocation.lat,
      lon: clinic.clinicLocation.lon
    }
    let distance = getClinicDisnt(GPS, clinicLocation)
    let text = {
      clinicName: clinic.clinicName,
      dist: distance.toFixed(2)
    }
    contents.push(text)
  }
  // 將存取到的資訊，透過迴圈打印出文字再push訊息出去
  dialogMessage.resultMessage = "您好，您目前與所有診所的距離為以下：\n" 
  for(let content of contents){
    dialogMessage.resultMessage += 
    `${countArray}.  ${content.clinicName} --> ${content.dist} 公里\n`
    countArray ++
  }
  dialogMessage.resultMessage += "==================="
  dialogMessage.event = event
  lineService.pushMessage(dialogMessage)

  dialogflow.dialogflowAgent(dialogMessage)
}

const getClinicDisnt = (GPS: any, clinicLocation: any): any =>{
  // 得到兩點經緯度座標之間的距離(公里)
  let R = 6378.137
  let dLat = deg2rad(clinicLocation.lat - GPS.lat)  // deg2rad below
  let dLon = deg2rad(clinicLocation.lon - GPS.lon)
  let a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(GPS.lat)) * Math.cos(deg2rad(clinicLocation.lat)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2)
  let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  let d = R * c // Distance in km
  return d
}

function deg2rad(deg) {
  return deg * (Math.PI / 180)
}

export const getOpenHours = async(dialogMessage: DialogMessage) =>{
  // 獲取門診營業時間
  let allClinic = await dataProxy.getClinics()
  for(let clinic of allClinic){
    if(dialogMessage.parameters.clinic == clinic.clinicName){
      dialogMessage.event = "openHoursSuccess"
      dialogMessage.parameters = {
        clinicName: clinic.clinicName,
        morning: clinic.openTime.morning,
        afternoon: clinic.openTime.afternoon,
        night: clinic.openTime.night
      }
    }
  }
  dialogflow.dialogflowAgent(dialogMessage)
}

export const bindNewMemberID = async(dialogMessage: DialogMessage) =>{
  const member = {} as Member
  const id = dialogMessage.userMessage
  const records = {} as Record
  const month = new Date().getMonth() + 1
  member.lineId = dialogMessage.lineId
  member.id = id
  databaseService.setNewMember(member)
  databaseService.setNewRecord(member, records, `${month}`)
}

export const bindNewMemberIformation = async(dialogMessage: DialogMessage) =>{
  // 綁定新用戶資訊
  let lineId = dialogMessage.lineId
  const member = await dataProxy.getMemberByLineId(lineId)
  // 根據用戶輸入再藉由dialog去判別用戶輸入的為哪些參數再一一放入
  member.name = dialogMessage.parameters.person.name
  member.phone = dialogMessage.parameters.phone
  member.email = dialogMessage.parameters.any + dialogMessage.parameters.email
  member.bufferMessage = ""
  dialogMessage.event = "bindNewMemberSuccess"
  dialogMessage.parameters = {
    id: member.id,
    name: member.name,
    phone: member.phone,
    email: member.email,
  }

  databaseService.updateMember(member)
  dialogflow.dialogflowAgent(dialogMessage)
}

export const diseaseKnowledge = async(dialogMessage: DialogMessage) =>{
  let dieaseName = dialogMessage.parameters.dieaseName
  const diease = await dataProxy.getDieaseByDieaseName(dieaseName)
  dialogMessage.event = "diseaseNameSuccess"
  dialogMessage.parameters.description = diease.description
  dialogflow.dialogflowAgent(dialogMessage)
}

export const getMemberData = async(dialogMessage: DialogMessage) =>{
  let contents
  let recordLen
  let memberName = dialogMessage.parameters.memberName
  let lineId = dialogMessage.lineId
  const authoriaztion = await verifyAuthorization(lineId, memberName)
  console.log("authoriaztion", authoriaztion)
  let event = ""

  if(authoriaztion){
    if(!memberName){
      members = await dataProxy.getMemberByLineId(dialogMessage.lineId)
      records = await dataProxy.getRecordsByMemberID(members.id)
      recordLen = await dataProxy.getRecordsLenght(members.id)
      contents = recordsFlexMessage(records)
      dialogMessage.event = "getMemberDataSuccess"
      dialogMessage.parameters = {
        name: members.name,
        recordsLen: recordLen
      }
    }else{
      members = await dataProxy.getMemberByMemberName(memberName)
      if(!members){
        dialogMessage.event = "memberNotFound"
      }else{
        records = await dataProxy.getRecordsByMemberID(members.id)
        contents = recordsFlexMessage(records)
        recordLen = await dataProxy.getRecordsLenght(members.id)
        dialogMessage.event = "getMemberDataSuccess"
        dialogMessage.parameters = {
          name: members.name,
          recordsLen: recordLen
        }
      }
    }
  }else{
    members = await dataProxy.getMemberByLineId(lineId)
    event = "notAuthorized"
    dialogMessage.event = event
    dialogMessage.parameters = {
      name: members.name,
      // recordsLen: recordLen
    }
  }

  if(contents){
    lineService.pushFlexMessage(dialogMessage, contents)
  }

  dialogflow.dialogflowAgent(dialogMessage)
}

const verifyAuthorization = async(lineId: string, memberName: string): Promise<any> => {
  const member = await dataProxy.getMemberByLineId(lineId)
  if (!memberName || member.name == memberName) {
    return 1

  } else if (member.name != memberName && member.role == "manager") {
    return 1


  } else if (member.name != memberName && member.role == "user") {
    return 0

  }
}

export const setMemberRole = async (dialogMessage: DialogMessage) => {
  const lineId = dialogMessage.lineId
  const member = await dataProxy.getMemberByLineId(lineId)
  const role = dialogMessage.parameters.role
  member.role = role
  await databaseService.updateMember(member)

  dialogMessage.event = "setMemberRoleSuccess"
  dialogMessage.parameters = {
    name: member.name,
    role: role
  }
  dialogflow.dialogflowAgent(dialogMessage)
}

