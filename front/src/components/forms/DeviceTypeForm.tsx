import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface DeviceTypeFormProps {
  tagSelectData?: DynamicOption[] | null;
  tag: DynamicOption | null;
  setTag: React.Dispatch<any>;
  deviceTypeName: null | string;
  setDeviceTypeName: React.Dispatch<any>;
  onClose: Function;
  updateTable: any;
}
const DeviceTypeForm = (props: DeviceTypeFormProps) => {
  const {
    tag,
    setTag,
    deviceTypeName,
    setDeviceTypeName,
    tagSelectData,
    onClose,
    updateTable,
  } = props;
  const createDeviceType = async () => {
    // //console.log("tag name :", tag);
    if (tag && deviceTypeName) {
      const json = {
        water_meter_type_name: deviceTypeName,
        water_meter_type_other_information: {},
        water_meter_tag: tag.value,
      };
      const data = new FormData();
      data.append("data", JSON.stringify(json));
      //   if (files.length > 0) {
      //     data.append("file", files[0]);
      //   }
      let response = await reqFunction("WaterMeterTypes/admin/add", data);
      if (response.code === 200) {
        renderToast("ایجاد نوع دستگاه با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        setDeviceTypeName("");
        setTag(null);
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ایجاد نوع دستگاه خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      <InputField
        id="device-type-name"
        label="نام نوع دستگاه"
        placeholder="نام نوع دستگاه را وارد کنید"
        type="text"
        state={deviceTypeName}
        setState={setDeviceTypeName}
      />
      <SelectInput
        label="دسته بندی"
        placeholder="دسته بندی مورد نظر را انتخاب کنید"
        dynamicOptions={tagSelectData}
        state={tag}
        setState={setTag}
      />
      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => createDeviceType()}
          text={`ایجاد نوع دستگاه`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default DeviceTypeForm;
