import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface OrderTypeFormProps {
  orderTypeName: null | string;
  setOrderTypeName: React.Dispatch<any>;
  onClose: Function;
  updateTable: any;
}
const OrderTypeForm = (props: OrderTypeFormProps) => {
  const { orderTypeName, setOrderTypeName, onClose, updateTable } = props;
  const createOrderType = async () => {
    // //console.log("tag name :", orderTypeName);
    if (orderTypeName) {
      let response = await reqFunction("OrderType/admin/create", {
        order_type_name: orderTypeName,
        order_type_information: {},
      });
      if (response.code === 200) {
        renderToast("ایجاد دستور با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        setOrderTypeName("");
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ایجاد دستور خطایی رخ داده",
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
        id="tag-name"
        label="نام دستور"
        placeholder="نام دستور را وارد کنید"
        type="text"
        state={orderTypeName}
        setState={setOrderTypeName}
      />

      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => createOrderType()}
          text={`ایجاد`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default OrderTypeForm;
