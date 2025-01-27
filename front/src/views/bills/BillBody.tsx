import BillCustomTable from "components/tables/BillCustomTable";
import { BillObject } from "./ShowBills";
import { toPersianDate } from "utils/TimeUtiles";
import moment from "moment";
import { renderUnit } from "utils/CommonFunctions";
interface BillBodyProps {
  info: BillObject;
  type: string;
}
const BillBody = ({ info, type }: BillBodyProps) => {
  const durationData = [
    "",
    toPersianDate(info.bill_start_date),
    toPersianDate(
      moment(info.bill_end_date, "YYYY-M-D")
        .subtract(1, "day")
        .format("YYYY-M-D")
    ),
  ];
  const counterData = [info.bill_water_meter.water_meter_serial, "فعال"];
  const consumptionData = [
    info.other_information.period_days,
    (type !== "گاز"
      ? info.consumptions / 1000
      : info.consumptions
    ).toLocaleString("fa-IR", {
      minimumFractionDigits: 3,
      maximumFractionDigits: 3,
    }),
    (
      (type !== "گاز" ? info.consumptions / 1000 : info.consumptions) /
      info.other_information.period_days
    ).toLocaleString("fa-IR", {
      minimumFractionDigits: 3,
      maximumFractionDigits: 3,
    }),
  ];
  const consumptionDetails = [
    info?.other_information?.start_period_sum
      ? info?.other_information?.start_period_sum.toLocaleString("fa-IR", {
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        })
      : info?.other_information?.start_period_sum,
    info?.other_information?.end_period_sum
      ? info?.other_information?.end_period_sum.toLocaleString("fa-IR", {
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        })
      : info?.other_information?.end_period_sum,
    info?.other_information?.bill_factor
      ? info?.other_information?.bill_factor
      : // ? 1
        1,
  ];
  const price = [
    "بهای میزان مصرف",
    Math.round(info.bill_price).toLocaleString("fa-IR", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }),
  ];
  const services = ["بهای خدمات", ""];
  const taxes = ["آبونمان", ""];
  const totalPrice = [
    "جمع صورتحساب دوره",
    // Math.round(info.bill_price).toLocaleString(),
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
            header={["دوره"]}
            body={[["نام دوره", "شروع دوره", "پایان دوره"], durationData]}
            hcolspan={"3"}
            type={type}
          />
          <BillCustomTable
            header={["سریال کنتور", "وضعیت کنتور"]}
            body={[counterData]}
            hcolspan={"1"}
            type={type}
          />
          <BillCustomTable
            classes="extra-bill-section"
            header={["شرح مصرف کنتور"]}
            body={[
              [
                `قرائت پیشین (${renderUnit(type, false)})`,
                `قرائت فعلی (${renderUnit(type, false)})`,
                "ضریب",
              ],
              consumptionDetails,
            ]}
            hcolspan={"3"}
            type={type}
          />
        </div>
        <div className="">
          <div
            className="border dark:!border-white"
            style={{
              margin: "0 6px",
              border: "1px solid #000",
              height: "calc(100% - 11px)",
              width: "100%",
            }}
          ></div>
        </div>
        <div className="">
          <BillCustomTable
            header={["مصرف"]}
            body={[
              [
                "طول دوره (روز)",
                `مصرف دوره (${renderUnit(type, true)})`,
                `میانگین مصرف (${renderUnit(type, true)})`,
              ],
              consumptionData,
            ]}
            hcolspan={"3"}
            type={type}
          />
          <BillCustomTable
            header={["شرح", "مبلغ (ریال)"]}
            body={[price, services, taxes, totalPrice]}
            hcolspan={"1"}
            type={type}
          />
        </div>
      </div>
    </>
  );
};
export default BillBody;
