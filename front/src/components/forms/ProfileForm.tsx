import CustomButton from "components/button";
// import FileUploader from "components/fields/ImageUpload";
import InputField from "components/fields/InputField";
// import { useState } from "react";
// import { useState } from "react";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface ProfileFormProps {
  adminName: null | string;
  setAdminName: React.Dispatch<any>;
  adminLastname: null | string;
  setAdminLastname: React.Dispatch<any>;
  adminPhoneNumber: null | string;
  profilePreview: string;
  setProfilePreview: React.Dispatch<string>;
  onClose: Function;
  update: Function;
}
export type ProfileObject = {
  admin_name: string;
  admin_lastname: string;
  other_information: {};
};
const ProfileForm = (props: ProfileFormProps) => {
  const {
    adminName,
    setAdminName,
    adminLastname,
    setAdminLastname,
    adminPhoneNumber,
    // profilePreview,
    // setProfilePreview,
    onClose,
    update,
  } = props;
  const editProfile = async () => {
    if (adminName && adminLastname) {
      const json: ProfileObject = {
        admin_name: adminName,
        admin_lastname: adminLastname,
        other_information: {},
      };
      const data = new FormData();
      data.append("data", JSON.stringify(json));
      let response = await reqFunction("admins/admin/setProfile", data);
      if (response.code === 200) {
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
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      {/* <FileUploader
        uploaderType="profilePicture"
        preview={profilePreview}
        setPreview={setProfilePreview}
      /> */}
      <InputField
        id="admin-name"
        label="نام"
        placeholder="نام را وارد کنید"
        type="text"
        state={adminName}
        setState={setAdminName}
      />
      <InputField
        id="admin-last-name"
        label="نام خانوادگی"
        placeholder="نام خانوادگی را وارد کنید"
        type="text"
        state={adminLastname}
        setState={setAdminLastname}
      />
      <InputField
        id="admin-mobile"
        label="شماره موبایل"
        placeholder="شماره موبایل را وارد کنید"
        type="text"
        disabled={true}
        state={adminPhoneNumber}
      />

      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => editProfile()}
          text={"تغییر"}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default ProfileForm;
