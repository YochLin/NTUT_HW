const Firestore = require('@google-cloud/firestore');
import * as firebaseAdmin from "firebase-admin"
import axios from 'axios'
import { Member} from '../firestore/model'
import { clinicId } from '../chatbot/chatBotConfig'

const dataBase = firebaseAdmin.firestore()

// const dataBase = new Firestore({
//     projectId: 'paas-249703',
//     keyFilename: 'src/firestore/dataBaseAccountKey.json',
//   });

const clinicCollection = dataBase.collection("Clinics");
const memberCollection = dataBase.collection("Members");
const dieaseCollection = dataBase.collection("Dieases");

// const memberCollection = (clinicId: string) => {
//   return clinicCollection.doc(clinicId).collection("Members")
// }

const recordCollection = (memberId: string) => {
  return memberCollection.doc(memberId).collection("Records")
}

// ======================================= Get Member =============================================
export const getMemberByLineId = async(lineId: string): Promise<any> => {
  let member = memberCollection.where("lineId", "==", lineId).get().then(snapshot => {
    console.log("snapshot: ", snapshot.docs[0].data())
    return snapshot.docs[0].data()
  }).catch(err => {
    console.log(err)
  })
  return member
}

export const getMemberByPhone = async (phone: string): Promise<any> => {
  let member = await memberCollection.where("phone", "==", phone).get().then(snapshot => {
    console.log("snapshot: ", snapshot.docs[0].data())
    return snapshot.docs[0].data()
  }).catch(err => {
    console.log(err)
  })
  return member
}

export const getMemberByID = async (id: string): Promise<any> => {
  let member = await memberCollection.where("id", "==", id).get().then(snapshot => {
    console.log("snapshot: ", snapshot.docs[0].data())
    return snapshot.docs[0].data()
  }).catch(err => {
    console.log(err)
  })
  return member
}

export const getMemberByMemberName = async (name: string): Promise<any> => {
  let member = await memberCollection.where("name", "==", name).get().then(snapshot => {
    console.log("snapshot: ", snapshot.docs[0].data())
    return snapshot.docs[0].data()
  }).catch(err => {
    console.log(err)
  })
  return member
}

// ======================================= Get Clinic =============================================
export const getClinicByClinicId = async(clinicId: string): Promise<any> => {
  let clinic = await clinicCollection.where("clinicId", "==", clinicId).get().then(snapshot =>{
    console.log("snapshot: ", snapshot.docs[0].data())
    return snapshot.docs[0].data()
  }).catch(err =>{
    console.log(err)
  })
  return clinic
}

export const getClinicByClinicName = async(clinicName: string): Promise<any> => {
  let clinic = await clinicCollection.where("clinicName", "==", clinicName).get().then(snapshot =>{
    console.log("snapshot: ", snapshot.docs[0].data())
    return snapshot.docs[0].data()
  }).catch(err =>{
    console.log(err)
  })
  return clinic
}

export const getClinics = () =>{
  const clinic = clinicCollection.get().then(snapshot =>{
    return snapshot.docs.map(doc => doc.data())
  })
  return clinic
}



// ======================================= Get Record =============================================
export const getRecordsByMemberID = async(memberId: string): Promise<any> =>{
  const month = new Date().getMonth() + 1
  const record = await recordCollection(memberId).doc(`${month}`).collection('Records').get().then(snapshot => {
      return snapshot.docs.map(doc => doc.data())
  })
  return record
}

export const getRecordsLenght = (memberId: string) => {
  const month = new Date().getMonth() + 1
  const recordLen = recordCollection(memberId).doc(`${month}`).collection('Records').get().then(snapshot =>{
    return snapshot.size - 1
  })
  return recordLen
}

// ======================================= Get Diease =============================================
export const getDieaseByDieaseName = async(dieaseName: string): Promise<any> => {
  let diease = await dieaseCollection.where("dieaseName", "==", dieaseName).get().then(snapshot =>{
    console.log("snapshot: ", snapshot.docs[0].data())
    return snapshot.docs[0].data()
  }).catch(err =>{
    console.log(err)
  })
  return diease
}