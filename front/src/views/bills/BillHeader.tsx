// import { HOST } from "../../utils/const";

import { toPersianDate } from "utils/TimeUtiles";
import { BillObject } from "./ShowBills";
interface BillHeaderProps {
  info: BillObject;
}
const BillHeader = (props: BillHeaderProps) => {
  const { info } = props;
  const HOST = process.env.REACT_APP_SAYAL_API_ENDPOINT_MAIN;
  const location = info.bill_water_meter.water_meter_location;
  // console.log(location);
  const projectLogo =
    info.bill_water_meter.water_meter_project_info.water_meter_project_urls
      .logo;
  const projectName =
    info.bill_water_meter.water_meter_project_info
      .water_meter_project_employer_description.name;
  const billDetail = info.other_information.hasOwnProperty("bill_details")
    ? info.other_information.bill_details
    : "";
  const counterName = info.bill_water_meter.water_meter_name;

  return (
    <>
      <div className="header-section" style={{ position: "relative" }}>
        <h4 style={{ fontWeight: "bold", textAlign: "center" }}>
          {projectName}
        </h4>
        <p
          style={{
            textAlign: "center",
            width: "80%",
            margin: "0 auto",
            padding: "8px 0",
          }}
        >
          {billDetail}
        </p>
        <div
          className="logo"
          style={{
            width: "85px",
            position: "absolute",
            top: "-10px",
            right: "8px",
          }}
        >
          <img
            style={{ width: "100%", objectFit: "contain" }}
            src={
              projectLogo.indexOf(HOST) !== -1
                ? projectLogo
                : HOST + projectLogo
            }
            alt={projectName}
          />
        </div>
        <div className="counter-info text-start dark:!border-white">
          <div>
            <div>
              <span>مشترک : </span>
              {counterName}
            </div>
            <div>
              <span>نشانی : </span>
              {typeof location === "string" && location
                ? location
                : typeof location === "object" && location
                ? "__"
                : "__"}
            </div>
          </div>
          <div>
            <div>
              <span>تاریخ صدور قبض : </span>
              {toPersianDate(info.bill_create_date)}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
export default BillHeader;
