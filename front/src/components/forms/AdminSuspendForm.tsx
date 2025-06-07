import { Checkbox } from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import { useState } from "react";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface SuspendAdminFormProps {
  adminName: null | string;
  adminLastname: null | string;
  adminPhoneNumber: null | string;
  adminId: null | string;
  setAdminId: React.Dispatch<any>;
  lockoutUntil: string | null;
  clearForm: Function;
  onClose: Function;
  updateTable: any;
}
const SuspendAdminForm = (props: SuspendAdminFormProps) => {
  const {
    adminName,
    adminLastname,
    adminPhoneNumber,
    clearForm,
    adminId,
    lockoutUntil,
    onClose,
    updateTable,
  } = props;

  const timeUnits: DynamicOption[] = [
    { value: "hours", label: "ساعت" },
    { value: "days", label: "روز" },
  ];

  const now = new Date();
  const lockoutDate = lockoutUntil ? new Date(lockoutUntil) : null;

  let remainingTime = "";
  if (lockoutDate && lockoutDate > now) {
    const diffMs = lockoutDate.getTime() - now.getTime();
    const diffHours = Math.ceil(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);
    remainingTime =
      diffDays > 0
        ? `${diffDays} روز باقی مانده`
        : `${diffHours} ساعت باقی مانده`;
  }

  const [suspendValue, setSuspendValue] = useState("");
  const [suspendUnit, setSuspendUnit] = useState<DynamicOption | null>(
    timeUnits[0]
  );

  const suspendAdmin = async () => {
    const json = {
      other_admin_id: adminId,
      suspend_time: `${suspendValue} ${suspendUnit?.value}`,
    };
    let response = await reqFunction("admins/admin/suspend", json);
    if (response.code === 200) {
      renderToast("تعلیق کاربر با موفقیت انجام شد", "success");
      updateTable();
      onClose();
      clearForm();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در تعلیق کاربر خطایی رخ داده",
        "err"
      );
    }
  };

  const removeSuspension = async () => {
    const json = {
      other_admin_id: adminId,
    };
    const response = await reqFunction("admins/admin/removeSuspension", json);
    if (response.code === 200) {
      renderToast("تعلیق کاربر برداشته شد", "success");
      updateTable();
      onClose();
      clearForm();
    } else {
      renderToast(response?.farsi_message || "خطا در حذف تعلیق کاربر", "err");
    }
  };

  return (
    <div className=" flex flex-col space-y-4">
      <InputField
        id="admin-name"
        label="نام کاربر"
        placeholder=""
        type="text"
        disabled={true}
        state={adminName}
      />
      <InputField
        id="admin-last-name"
        label="نام خانوادگی مدیر"
        placeholder=""
        type="text"
        disabled={true}
        state={adminLastname}
      />
      <InputField
        id="admin-mobile"
        label="شماره موبایل"
        placeholder=""
        type="text"
        disabled={true}
        state={adminPhoneNumber}
      />
      {lockoutDate && lockoutDate > new Date() ? (
        <div className="font-bold text-red-600">{remainingTime}</div>
      ) : (
        <div className="flex gap-2 space-x-4">
          <SelectInput
            dynamicOptions={timeUnits}
            label="واحد"
            state={suspendUnit}
            setState={setSuspendUnit}
          />
          <InputField
            id="suspend-value"
            label="مدت تعلیق"
            placeholder="مثلا 12"
            type="number"
            state={suspendValue}
            setState={setSuspendValue}
          />
        </div>
      )}

      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={removeSuspension}
          text="برداشتن تعلیق"
          color="blue"
          extra="!ml-2"
        />

        <CustomButton
          onClick={() => suspendAdmin()}
          text={"تعلیق کاربر"}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default SuspendAdminForm;
