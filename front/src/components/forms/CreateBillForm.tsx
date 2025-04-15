import CustomButton from "components/button";
import DateInput from "components/fields/DateInput";
import InputField from "components/fields/InputField";
import { DynamicOption } from "components/fields/SelectInput";
import { useState } from "react";
import { reqFunction } from "utils/API";
import { getToday } from "utils/TimeUtiles";
import { renderToast } from "utils/globalUtils";

interface CreateBillFormProps {
  project: DynamicOption;
  tag: DynamicOption;
  selectedDevices: string[];
  billDescription: string;
  setBillDescription: React.Dispatch<any>;
  payDescription: string;
  setPayDescription: React.Dispatch<any>;
  onClose: Function;
}
type DetailObject = {
  english_message: string;
  farsi_message: string;
  meter_serial: string;
};
type BillResult = {
  all_meters_inputed: number;
  all_bill_successfully_created: {
    count: number;
    details: DetailObject[];
  };
  all_bill_not_created: {
    count: number;
    details: DetailObject[];
  };
};
const CreateBillForm = (props: CreateBillFormProps) => {
  const [billTextBorder, setBillTextBorder] = useState<
    "err" | "success" | "dis" | "normal"
  >("normal");
  const [payTextBorder, setPayTextBorder] = useState<
    "err" | "success" | "dis" | "normal"
  >("normal");
  const [fromDate, setFromDate] = useState(getToday().jDate(1));
  const [tillDate, setTillDate] = useState(getToday());
  const [payDate, setPayDate] = useState(getToday().add(10, "day"));
  const {
    project,
    tag,
    payDescription,
    setPayDescription,
    billDescription,
    setBillDescription,
    selectedDevices,
    onClose,
  } = props;
  const clearForm = () => {
    setPayDescription("");
    setBillDescription("");
  };
  const createBill = async () => {
    if (billDescription && payDescription) {
      setPayTextBorder("normal");
      setBillTextBorder("normal");
      const data = {
        meter_serial_list: selectedDevices,
        calculate_method: "from_project",
        project_id: project.value,
        tag_id: tag.value,
        payment_dead_line: payDate.format("YYYY-M-D"),
        start_time: fromDate.format("YYYY-M-D"),
        end_time: tillDate.add(1, "day").format("YYYY-M-D"),
        other_information: {
          bill_details: billDescription,
          pay_details: payDescription,
        },
      };
      let response = await reqFunction("bills/admin/createBill/list", data);
      // //console.log(response);
      if (response.code === 200) {
        // //console.log(response.data);
        let result: BillResult = response.data;
        result.all_meters_inputed !== result.all_bill_successfully_created.count
          ? result.all_bill_not_created.details.forEach((res) =>
              renderToast(`(${res.meter_serial}) ${res.farsi_message}`, "err")
            )
          : renderToast("صدور قبوض با موفقیت انجام شد", "success");
        onClose();
        clearForm();
      } else if (response.code === 444) {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در صدور قبض خطایی رخ داده",
          "err"
        );
      }
    } else {
      if (!billDescription) {
        renderToast("توضیحات قبض باید وارد شود", "warn");
        setBillTextBorder("err");
        setPayTextBorder("normal");
      }
      if (!payDescription) {
        renderToast("توضیحات پرداخت باید وارد شود", "warn");
        setPayTextBorder("err");
        setBillTextBorder("normal");
      }
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      <DateInput label="تاریخ شروع" value={fromDate} onChange={setFromDate} />
      <DateInput label="تاریخ پایان" value={tillDate} onChange={setTillDate} />
      <DateInput label="مهلت پرداخت" value={payDate} onChange={setPayDate} />
      <InputField
        id="bill-description"
        label="توضیحات قبض"
        placeholder="توضیحات قبض را وارد کنید"
        type="text-aria"
        state={billDescription}
        setState={setBillDescription}
        border={billTextBorder}
      />
      <InputField
        id="pay-description"
        label="توضیحات پرداخت"
        placeholder="توضیحات پرداخت را وارد کنید"
        type="text-aria"
        state={payDescription}
        setState={setPayDescription}
        border={payTextBorder}
      />
      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => createBill()}
          text={`صدور`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default CreateBillForm;
