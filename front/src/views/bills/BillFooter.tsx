import { toPersianDate } from "utils/TimeUtiles";
import { BillObject } from "./ShowBills";
import Num2persian from "num2persian";
import BillCustomTable from "components/tables/BillCustomTable";
import { renderUnit } from "utils/CommonFunctions";
interface BillFooterProps {
  info: BillObject;
  type: string;
  patternSample: { k: string; v1: string; v2: string }[];
}
const BillFooter = ({ info, type, patternSample }: BillFooterProps) => {
  // //console.log(Num2persian());
  const textPrice = [`${Num2persian(Math.round(info.bill_price))} ریال`];
  const payDetails = info.other_information.hasOwnProperty("pay_details")
    ? info.other_information.pay_details
    : "";
  const paymentInfo = [info.bill_serial, ""];
  const unitsInfo = [
    `نرخ هر (${renderUnit(
      info.bill_water_meter.water_meter_type_info.water_meter_tag_info
        .water_meter_tag_name,
      true
    )})`,
    Number(patternSample[0]?.k).toLocaleString("fa-IR", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }),
    // info.bill_water_meter.water_meter_type_info.water_meter_tag_info
    //   .water_meter_tag_name === "برق"
    //   ? "4548"
    //   : "__",
  ];
  const paymentDeadline = [
    toPersianDate(info.payment_dead_line),
    Math.round(info.bill_price).toLocaleString("fa-IR", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }),
  ];
  return (
    <>
      <div className="container grid grid-cols-3 gap-5">
        <div className="">
          <BillCustomTable
            header={["بهای واحد مصرف (ریال)"]}
            body={[unitsInfo]}
            hcolspan={"2"}
            type={type}
          />
        </div>
        <div className="">
          <div style={{ margin: "0 6px 0 0" }}>
            <BillCustomTable
              header={["شناسه قبض", "شناسه پرداخت "]}
              body={[paymentInfo]}
              hcolspan={"1"}
              type={type}
            />
          </div>
        </div>
        <div className="">
          <BillCustomTable
            header={["مهلت پرداخت", "مبلغ قابل پرداخت (ریال)"]}
            body={[paymentDeadline]}
            hcolspan={"1"}
            type={type}
          />
        </div>
      </div>
      <div className="last text-start">
        <div
          className="border border-solid dark:!border-white"
          style={{
            padding: "3px",
            margin: "3px 0",
            border: "1px solid #000",
          }}
        >
          مبلغ به حروف : <span style={{ padding: "0 5px" }}>{textPrice}</span>
        </div>
        <div className="pt-4" style={{ textAlign: "start" }}>
          {payDetails}
        </div>
      </div>
    </>
  );
};
export default BillFooter;
