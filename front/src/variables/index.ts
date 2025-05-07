import { checkInputData } from "components/fields/CheckInput";
import { DynamicOption } from "components/fields/SelectInput";
export type CountOption ={
    label:string;
    value:number;
    
}
export const importanceSelectData: DynamicOption[] = [
     { label: "زیاد" ,value:"H"},
    { label: "متوسط" ,value:"M"},
    { label: "کم" ,value:"L"},
] 
export const deviceOrderModesSelectData: DynamicOption[] = [
    { label: "فرمان زنده (منبع برق)" ,value:"R"},
    { label: "فرمان زمان دار (منبع باتری)" ,value:"P"},
] 
export const counterTagSelect: DynamicOption[] = [
    { label: "آب" ,value:"07d00e58-a3a4-4963-9f25-d22d4a5befbd"},
   { label: "برق" ,value:"ac32c39a-c371-4936-a802-37ead17f8301"},
   { label: "گاز" ,value:"3d5fd998-2637-4a61-a469-4bb344417cc5"},
] 
export const simOprators: DynamicOption[] = [
    { label: "همراه اول" ,value:"mci"},
   { label: "ایرانسل" ,value:"mtn"},
   { label: "رایتل" ,value:"righttel"},
] 
export const counterModels: DynamicOption[] = [
    { label: "MD" ,value:"md"},
   { label: "SD" ,value:"sd"},
   { label: "CD" ,value:"cd"},
   { label: "WPI" ,value:"wpi"},
   { label: "WP" ,value:"wp"},
] 
export const moduleAttributes:checkInputData[] = [
    {id:"1",name:"ارسال اطلاعات"},
    {id:"2",name:"فرمان پذیری"},
    {id:"3",name:"ارسال اطلاعات مکانی(GPS)"},
    {id:"4",name:"پورت نوری"}
]
export const counterSizes: CountOption[] = [
    { label: "1/2 اینچ" ,value:1},
   { label: "3/4 اینچ" ,value:2},
   { label: "1 اینچ" ,value:3},
   { label: "1 و 1/4 اینچ" ,value:4},
   { label: "1 و 1/2 اینچ" ,value:5},
   { label: "2 اینچ" ,value:6},
   { label: "3 اینچ" ,value:7},
   { label: "4 اینچ" ,value:8},
   { label: "5 اینچ" ,value:9},
   { label: "6 اینچ" ,value:10},
   { label: "8 اینچ" ,value:11},
   { label: "10 اینچ" ,value:12},
   { label: "12 اینچ" ,value:13},
] 
export const sortValueSelect: DynamicOption[] = [
    { label: "تاریخ ثبت آخرین مصرف" ,value:"last_cons_object_create_time"},
   { label: "میزان آخرین مصرف" ,value:"last_consumption_value"},
   { label: "مصرف ماه جاری" ,value:"month"},
   { label: "مصرف سال جاری" ,value:"year"},
] 
export const reversedSelect: DynamicOption[] = [
    { label: "نزولی" ,value:true},
   { label: "صعودی" ,value:false},
] 
export const countSelect: CountOption[] = [
    { label: "100 عدد" ,value:100},
    { label: "50 عدد" ,value:50},
    { label: "150 عدد" ,value:150},
   { label: "200 عدد" ,value:200},
]
export const cities:DynamicOption[]=[
    { label: "سراسر کشور" ,value:"سراسر کشور"},
    { label: "تهران" ,value:"تهران"},
    { label: "مشهد" ,value:"مشهد"},
    { label: "شیراز" ,value:"شیراز"},
    { label: "قم" ,value:"قم"},
    { label: "اراک" ,value:"اراک"},
    { label: "اردبیل" ,value:"اردبیل"},
    { label: "ارومیه" ,value:"ارومیه"},
    { label: "اصفهان" ,value:"اصفهان"},
    { label: "اهواز" ,value:"اهواز"},
    { label: "ایلام" ,value:"ایلام" },
    { label: "بجنورد" ,value:"بجنورد"},
    { label: "بندرعباس" ,value:"بندرعباس"},
    { label: "بوشهر" ,value:"بوشهر"},
    { label: "بیرجند" ,value:"بیرجند"},
    { label: "تبریز" ,value:"تبریز"},
    { label: "خرم آباد" ,value:"خرم آباد"},
    { label: "رشت" ,value:"رشت" },
    { label: "زاهدان" ,value:"زاهدان"},
    { label: "زنجان" ,value:"زنجان"},
    { label: "ساری" ,value:"ساری"},
    { label: "سمنان" ,value:"سمنان"},
    { label: "سنندج" ,value:"سنندج"},
    { label: "شهرکرد" ,value:"شهرکرد"},
    { label: "قزوین" ,value:"قزوین"},
    { label: "کرج" ,value:"کرج"},
    { label: "کرمان" ,value:"کرمان"},
    { label: "کرمانشاه" ,value:"کرمانشاه"},
    { label: "گرگان" ,value:"گرگان"},
    { label: "همدان" ,value:"همدان"},
    { label: "یاسوج" ,value:"یاسوج"},
    { label: "یزد" ,value:"یزد" },
  ];