// export type Register = {
//     id: string,
//     lineId: string,
//     numberSlip: number,
//     registerLocation: {
//         lat: number,
//         lon: number
//     },
//     member: Member[],
//     report: Report[]
//   }
  
  export type Member = {
    id: string,
    name: string,
    lineId: string,
    phone: string,
    email: string,
    bufferMessage: string,
    role: string,
    records?: Record[]
  }

  // export type Report = {
  //   id: string,
  //   lineId: string,
  //   registerDay: string,
  //   registerCount: number
  // }
  
  export type Record = {
    month: string,
    registerDay: string,
    registerTime: string,
    registerTimeState?: number,
    department: string,
    registerStore: string
  }

  export type Clinic = {
    clinicId: string,
    clinicName: string,
    openTime: {
      morning: string,
      afternoon: string,
      night: string
    },
    clinicLocation: {
      lat: number,
      lon: number
    },
  departments: Array<any>
  }
