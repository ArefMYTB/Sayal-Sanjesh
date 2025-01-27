import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import { useState } from "react";
import { reqFunction } from "utils/API";
import { isPhoneValid, renderToast, toEnglish } from "utils/globalUtils";

interface UserFormProps {
  userName: null | string;
  setUserName: React.Dispatch<any>;
  userLastname: null | string;
  setUserLastname: React.Dispatch<any>;
  userPhoneNumber: null | string;
  setUserPhoneNumber: React.Dispatch<any>;
  onClose: Function;
  updateTable: any;
}
export type userObject = {
  user_name: null | string;
  user_phone: null | string;
  user_lastname: null | string;
  user_password: null;
  user_sms_code: null;
  other_information: {
    description: null | string;
  };
  user_profile: {
    default: null | string;
  };
};
const UserForm = (props: UserFormProps) => {
  const [phoneBorder, setPhoneBorder] = useState<
    "err" | "success" | "dis" | "normal"
  >("normal");
  const {
    userName,
    setUserName,
    userLastname,
    setUserLastname,
    userPhoneNumber,
    setUserPhoneNumber,
    onClose,
    updateTable,
  } = props;
  const clearForm = () => {
    setUserName("");
    setUserLastname("");
    setUserPhoneNumber("");
  };
  const createUser = async () => {
    if (userName && userLastname && userPhoneNumber) {
      if (isPhoneValid(userPhoneNumber)) {
        const json: userObject = {
          user_name: userName,
          user_phone: toEnglish(userPhoneNumber),
          user_lastname: userLastname,
          user_password: null,
          user_sms_code: null,
          other_information: {
            description: "",
          },
          user_profile: {
            default: "default",
          },
        };
        const data = new FormData();
        data.append("data", JSON.stringify(json));
        let response = await reqFunction("users/admin/add", data);
        if (response.code === 200) {
          renderToast("ایجاد کاربر با موفقیت انجام شد", "success");
          updateTable();
          onClose();
          clearForm();
        } else {
          renderToast(
            response?.farsi_message
              ? response.farsi_message
              : "در ایجاد کاربر خطایی رخ داده",
            "err"
          );
        }
      } else {
        renderToast("شماره تماس 11 رقم بوده و با 0 شروع میگردد", "warn");
        setPhoneBorder("err");
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      <InputField
        id="user-name"
        label="نام کاربر"
        placeholder="نام کاربر را وارد کنید"
        type="text"
        state={userName}
        setState={setUserName}
      />
      <InputField
        id="tag-last-name"
        label="نام خانوادگی کاربر"
        placeholder="نام خانوادگی کاربر را وارد کنید"
        type="text"
        state={userLastname}
        setState={setUserLastname}
      />
      <InputField
        id="user-mobile"
        label="شماره موبایل"
        placeholder="شماره موبایل را وارد کنید"
        type="text"
        state={userPhoneNumber}
        setState={setUserPhoneNumber}
        border={phoneBorder}
      />

      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => createUser()}
          text={`ایجاد`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default UserForm;
