import CustomButton from "components/button";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface OrderFormProps {
  orderTypeSelectData?: DynamicOption[] | null;
  deviceSelectData?: DynamicOption[] | null;
  onClose: Function;
  orderType: null | DynamicOption;
  device: null | DynamicOption;
  setOrderType: React.Dispatch<any>;
  setDevice: React.Dispatch<any>;
  updateTable: any;
}
const OrdersForm = (props: OrderFormProps) => {
  const {
    onClose,
    deviceSelectData,
    orderTypeSelectData,
    device,
    setDevice,
    orderType,
    setOrderType,
    updateTable,
  } = props;
  const createOrder = async () => {
    // //console.log("orderType :", orderType);
    // //console.log("device :", device);
    if (device && orderType) {
      let response = await reqFunction("Order/admin/create", {
        // order_type_id: orderType.value,
        order_type_id_list: [orderType.value],
        water_meter_serial: device.value,
        order_information: {},
      });
      if (response.code === 200) {
        renderToast("ارسال دستور با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        setDevice(null);
        setOrderType(null);
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ارسال دستور خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("تمامی موارد را انتخاب کنید", "warn");
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      <SelectInput
        label="نام دستور"
        placeholder="دستور مورد نظر را انتخاب کنید"
        dynamicOptions={orderTypeSelectData}
        state={orderType}
        setState={setOrderType}
      />
      <SelectInput
        label="نام دستگاه"
        placeholder="دستگاه مورد نظر را انتخاب کنید"
        dynamicOptions={deviceSelectData}
        state={device}
        setState={setDevice}
      />

      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => createOrder()}
          text={`ارسال`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default OrdersForm;
