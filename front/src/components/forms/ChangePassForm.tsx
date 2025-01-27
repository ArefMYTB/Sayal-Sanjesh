import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import { useState } from "react";
// import { useState } from "react";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface ChangePassFormProps {
  onClose: Function;
  update: Function;
}
export type PasswordObject = {
  admin_password: string;
  admin_old_password: string;
};
const ChangePassForm = (props: ChangePassFormProps) => {
  const [border, setBorder] = useState<"err" | "success" | "dis" | "normal">(
    "normal"
  );
  const { onClose, update } = props;
  const [userPassword, setUserPassword] = useState<string>("");
  const [userNewPassword, setUserNewPassword] = useState<string>("");
  const [userConfirmPassword, setUserConfirmPassword] = useState<string>("");
  const changePassword = async () => {
    if (userPassword && userNewPassword && userConfirmPassword) {
      if (userNewPassword === userConfirmPassword) {
        const json: PasswordObject = {
          admin_password: userConfirmPassword,
          admin_old_password: userPassword,
        };
        let response = await reqFunction("admins/admin/changePassword", json);
        if (response.code === 200) {
          setBorder("normal");
          renderToast("تغییر پروفابل با موفقیت انجام شد", "success");
          update();
          onClose();
        } else {
          renderToast(
            response?.farsi_message
              ? response.farsi_message
              : "در تغییرات پروفایل خطایی رخ داده",
            "err"
          );
        }
      } else {
        renderToast("گذرواژه جدید و تکرار آن یکسان نیست", "warn");
        setBorder("err");
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      <InputField
        id="admin-mobile"
        label="گذرواژه قدیم"
        placeholder="گذرواژه قدیم را وارد کنید"
        type="password"
        state={userPassword}
        setState={setUserPassword}
      />
      <InputField
        id="admin-name"
        label="گذرواژه جدید"
        placeholder="گذرواژه جدید را وارد کنید"
        type="password"
        state={userNewPassword}
        setState={setUserNewPassword}
        border={border}
      />
      <InputField
        id="admin-last-name"
        label="تکرار گذرواژه جدید"
        placeholder="گذرواژه جدید را مجدد وارد کنید"
        type="password"
        state={userConfirmPassword}
        setState={setUserConfirmPassword}
        border={border}
      />

      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => changePassword()}
          text={"تغییر"}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default ChangePassForm;
