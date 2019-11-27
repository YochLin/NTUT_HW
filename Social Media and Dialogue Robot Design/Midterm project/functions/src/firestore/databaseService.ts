const Firestore = require('@google-cloud/firestore');
import * as firebaseAdmin from "firebase-admin"
import * as functions from 'firebase-functions'
import * as cors from 'cors'
import { clinicId } from '../chatbot/chatBotConfig'
import { Member, Record, Clinic} from './model'

const dataBase = firebaseAdmin.firestore()

// const dataBase = new Firestore({
//     projectId: 'paas-249703',
//     keyFilename: 'src/firestore/dataBaseAccountKey.json',
//   });

const clinicCollection = dataBase.collection("Clinics");
const memberCollection = dataBase.collection("Members");
const dieaseCollection = dataBase.collection("Dieases");

// const memberCollection = (clinicId: string) =>{
//     return dataBase.collection("Clinics").doc(clinicId).collection("Members")
// }
const recordCollection = (memberId: string) =>{
    return memberCollection.doc(memberId).collection("Records")
}


const corsHandler = cors({ origin: true })
export const databaseService = functions.https.onRequest((req, res) => {
    corsHandler(req, res, async () => {
        console.log(req.path)
        switch (req.path) {
    
            case "/member":
                createMember(req, res)
                break
            case "/clinic":
                createClinic(req, res)
                break
            case "/record":
                createRecord(req, res)
                break
            case "/diease":
                createDiease(req, res)
            default:
                res.sendStatus(400)
                break
        }
    })
})


// ================================================= Create =========================================
function createMember(req: any, res: any) {
    const members = req.body.members as any
        for (let member of members) {
            memberCollection.doc(member.id).set(member)
        }
    res.status(200).send("OK")
}

function createClinic(req: any, res: any){
    const clinics = req.body.clinics as any
        for(let clinic of clinics){
            clinicCollection.doc(clinic.clinicId).set(clinic)
        }
    res.status(200).send("OK")
}

function createRecord(req: any, res: any){
    let countMonth = 0
    const records = req.body.records as any
    let setMonth = records[0].month
        for(let record of records){
            if(setMonth == record.month){
              recordCollection('N124859305').doc(`${record.month}`).collection('Records').doc(`${countMonth}`).set(record)
            }else {
              countMonth = 0
              setMonth = record.month
              recordCollection('N124859305').doc(`${record.month}`).collection('Records').doc(`${countMonth}`).set(record)
            }
            countMonth ++
        }
    res.status(200).send("OK")
}

function createDiease(req: any, res: any){
  const dieases = req.body.dieases as any
      for(let diease of dieases){
        dieaseCollection.doc(diease.dieaseName).set(diease)
      }
  res.status(200).send("OK")
}

// =============================== update ======================================
export const updateClinic = async(clinicId: string, clinic: Clinic): Promise<any> =>{
    clinicCollection.doc(clinicId).update(clinic).then(async() =>{
        console.log("Clinic database successfully updated!");
    }).catch(err =>{
        console.log(err)
    })
}

export const updateMember = async(member: Member): Promise<any> =>{
    memberCollection.doc(member.id).update(member).then(async() =>{
      console.log("Document successfully written!");
    }).catch(err => {
      console.log(err)
    })
  }

  // ================================================= set =========================================
  export const setNewMember = async(member: Member): Promise<any> =>{
    memberCollection.doc(member.id).set(member).then(async =>{
      console.log("New member set down!")
    }).catch(err =>{
      console.log(err)
    })
  }

  export const setNewRecord = async(member:Member, records: Record, month:string): Promise<any> =>{
    recordCollection(member.id).doc(`${month}`).collection('Records').doc("0").set(records).then(async =>{
      console.log("New record set down!")
    }).catch(err =>{
      console.log(err)
    })
}

export const setRecord = async(member:Member, records: Record): Promise<any> =>{
  const recordLen = await recordCollection(member.id).doc(records.month).collection('Records').get().then(snapshot =>{
    return snapshot.size
  })
  console.log("SetRecord", recordLen)
  recordCollection(member.id).doc(records.month).collection('Records').doc(`${recordLen}`).set(records).then(async =>{
    console.log("set record set down!")
  }).catch(err =>{
    console.log(err)
  })
}
