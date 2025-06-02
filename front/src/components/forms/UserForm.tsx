import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import { isPhoneValid, renderToast, toEnglish } from "utils/globalUtils";
import { DynamicOption } from "components/fields/SelectInput";
import { DeviceObj } from "views/counters";
import { ProjectObject } from "views/projects";
import SelectInput from "components/fields/SelectInput";

// Assigns a device (counter) to a user using serial and user ID
export const assignCounterToUser = async ({
  serial,
  userId,
}: {
  serial: string;
  userId: string;
}) => {
  try {
    const payload = {
      water_meter_serial: serial,
      water_meter_user_id: userId,
    };

    const response = await reqFunction("watermeters/admin/assignUser", payload);

    if (response.code === 200) {
      renderToast("مالک دستگاه با موفقیت تغییر یافت", "success");
    } else {
      renderToast(response?.farsi_message || "خطا در تغییر مالک دستگاه", "err");
    }
  } catch (error) {
    renderToast("مشکلی در ارتباط با سرور رخ داد", "err");
  }
};

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
  const [project, setProject] = useState<DynamicOption | null>(null);
  const [counter, setCounter] = useState<DynamicOption | null>(null);

  const {
    data: projectsData,
    isLoading: projectsIsLoading,
    status: projectsStatus,
  } = useQuery({
    queryKey: ["projectList"],
    queryFn: () =>
      reqFunction("WaterMeterProjectsURL/admin/getAll", {
        page: 1,
        count: 100,
        water_meter_project_name: null,
        water_meter_project_create_date: null,
        user_id: null,
      }),
  });

  const renderProjectSelect = (projectList: ProjectObject[]): DynamicOption[] =>
    projectList?.map((p) => ({
      label: p.water_meter_project_name,
      value: p.water_meter_project_id,
    }));

  const {
    data: countersData,
    isLoading: countersIsLoading,
    status: countersStatus,
  } = useQuery({
    queryKey: ["countersList", project],
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: 1,
        count: 1000,
        project_id: project?.value ?? null,
        water_meter_serial: null,
        user_id: null,
      }),
    enabled: !!project, // run only if project is selected
  });

  const renderCounterSelect = (list: DeviceObj[]): DynamicOption[] =>
    list?.map((d) => ({
      label: d.water_meter_name,
      value: d.water_meter_serial,
    }));

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
          assignCounterToUser({
            serial: counter.label,
            userId: response?.data?.userID,
          });

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
      {projectsStatus === "success" && (
        <SelectInput
          label="پروژه"
          placeholder="پروژه را انتخاب کنید"
          dynamicOptions={renderProjectSelect(projectsData?.data)}
          state={project}
          setState={setProject}
        />
      )}

      {countersStatus === "success" && (
        <SelectInput
          label="کنتور"
          placeholder="کنتور را انتخاب کنید"
          dynamicOptions={renderCounterSelect(countersData?.data)}
          state={counter}
          setState={setCounter}
          disabled={!project}
        />
      )}

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
