// import { toPersianDate } from "utils/TimeUtiles";
import Widget from "views/rtl/default/components/Widget";
import { OneDeviceObj } from ".";
import { renderUnit } from "utils/CommonFunctions";
import { useState } from "react";
import CheckInput from "components/fields/CheckInput";
import GetLocationMap from "components/map/GetLocationMap";
interface DeviceInformationProps {
  deviceInfo: [OneDeviceObj];
}
const DeviceInformation = (props: DeviceInformationProps) => {
  const { deviceInfo } = props;
  const info = deviceInfo[0];
  const [hasManualLocation, setHasManualLocation] = useState<string[]>(
    typeof info?.water_meter_location !== "string" &&
      info?.water_meter_location?.lat
      ? ["manual-location"]
      : []
  );
  const [lat, setLat] = useState<number | null>(
    typeof info?.water_meter_location !== "string" &&
      info?.water_meter_location?.lat
      ? Number(info.water_meter_location.lat)
      : 35.724096
  );
  const [lng, setLng] = useState<number | null>(
    typeof info?.water_meter_location !== "string" &&
      info?.water_meter_location?.lng
      ? Number(info.water_meter_location.lng)
      : 51.430389
  );
  return (
    <div className="projects-overview py-4 pt-2">
      <div className="pb-2 text-xl font-bold text-navy-700 dark:text-white">
        جزئیات دستگاه
      </div>
      <div className=" mt-3 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
        <Widget title={"نام دستگاه"} subtitle={info.water_meter_name} />
        <Widget title={"سریال دستگاه"} subtitle={info.water_meter_serial} />
        <Widget
          title={"پروژه دستگاه"}
          subtitle={
            info.water_meter_project_info?.project_name
              ? info.water_meter_project_info.project_name
              : "__"
          }
        />
        <Widget
          title={"دسته بندی"}
          subtitle={info.water_meter_tag_info.water_meter_tag_name}
        />
        <Widget
          title={"نوع دستگاه"}
          subtitle={info.water_meter_type_info.water_meter_type_name}
        />
        <Widget
          title={"کد ماژول"}
          subtitle={
            info.water_meter_module_info?.water_meter_module_id
              ? info.water_meter_module_info.water_meter_module_code
              : "__"
          }
        />
        <Widget
          title={"نام خریدار"}
          subtitle={
            info.water_meter_user_info?.user_id
              ? `${info.water_meter_user_info.user_name} ${info.water_meter_user_info.user_lastname}`
              : "__"
          }
        />
        <Widget
          title={"عدد مکانیکی"}
          subtitle={`${info.water_meter_manual_number} ${renderUnit(
            info.water_meter_tag_info.water_meter_tag_name,
            false
          )}`}
        />
        {/* <Widget
          title={"دستور پذیری"}
          subtitle={
            info.water_meter_order_mode === "P"
              ? "فرمان زمان دار (منبع باتری)"
              : info.water_meter_order_mode === "R"
              ? "فرمان زنده (منبع برق)"
              : "__"
          }
        /> */}
      </div>
      {/* <div className="pb-4 text-xl font-bold text-navy-700 dark:text-white">
        موقعیت مکانی
      </div> */}
      <div className=" pt-2">
        {" "}
        <CheckInput
          inputsData={[
            { id: "manual-location", name: "ایجاد موقعیت مکانی به صورت دستی" },
          ]}
          checkedData={hasManualLocation}
          setCheckedData={setHasManualLocation}
        />
      </div>
      {hasManualLocation.length > 0 ? (
        <GetLocationMap
          lat={lat}
          setLat={setLat}
          lng={lng}
          setLng={setLng}
          isInfo={true}
          deviceLoc={
            typeof info?.water_meter_location !== "string" &&
            info?.water_meter_location?.lat
              ? {
                  lat: Number(info.water_meter_location.lat),
                  lng: Number(info.water_meter_location.lng),
                }
              : null
          }
        />
      ) : (
        <></>
      )}
    </div>
  );
};
export default DeviceInformation;
