import CustomButton from "components/button";
import { DynamicOption } from "components/fields/SelectInput";
import { DeviceObj } from "views/counters";
import { ProjectObject } from "views/projects";
import { AdminsObject } from "views/users/AdminsTable";
import { UserObject } from "views/users/UsersTable";
import { ModuleObject } from "views/warehouse/ModuleStorage";

interface DeleteFormProps {
  deleteType:
    | "project"
    | "user"
    | "admin"
    | "simpleCounter"
    | "module"
    | "consumptions";
  projectDeleted?: ProjectObject;
  userDeleted?: UserObject;
  adminDeleted?: AdminsObject;
  simpleCounterDeleted?: DeviceObj;
  moduleDeleted?: ModuleObject;
  counterConsuptionDeleted?: DynamicOption;
  onClose: Function;
  deleteFunction: Function;
}
const DeleteForm = (props: DeleteFormProps) => {
  const {
    onClose,
    deleteFunction,
    projectDeleted,
    userDeleted,
    adminDeleted,
    simpleCounterDeleted,
    moduleDeleted,
    deleteType,
    counterConsuptionDeleted,
  } = props;
  return (
    <div className=" flex flex-col space-y-4 font-bold">
      <div className="">
        {" "}
        {`شما در حال حذف ${
          deleteType === "project"
            ? "پروژه"
            : deleteType === "admin"
            ? "کاربر سیستم"
            : deleteType === "user"
            ? "بهره بردار"
            : deleteType === "simpleCounter"
            ? "کنتور غیرهوشمند"
            : deleteType === "module"
            ? "ماژول"
            : "مقادیر مصرف"
        } "${
          deleteType === "project"
            ? projectDeleted.water_meter_project_name
            : deleteType === "user"
            ? `${userDeleted.user_name} ${userDeleted.user_lastname}`
            : deleteType === "admin"
            ? `${adminDeleted.admin_name} ${adminDeleted.admin_lastname}`
            : deleteType === "simpleCounter"
            ? `${simpleCounterDeleted.water_meter_name}`
            : deleteType === "module"
            ? `${moduleDeleted.water_meter_module_name}`
            : `${counterConsuptionDeleted.label}`
        }" هستید.`}
      </div>
      <div className="">در صورت حذف ، اطلاعات مربوطه قابل بازگشت نمی باشد.</div>
      <div className="">
        آیا از حذف{" "}
        {deleteType === "project"
          ? "پروژه"
          : deleteType === "admin"
          ? "کاربر سیستم"
          : deleteType === "user"
          ? "بهره بردار"
          : deleteType === "simpleCounter"
          ? "کنتور غیرهوشمند"
          : deleteType === "module"
          ? "ماژول"
          : "مقادیر مصرف"}{" "}
        اطمینان دارید؟!{" "}
      </div>
      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="blue" />
        <CustomButton
          onClick={() =>
            deleteFunction(
              deleteType === "project"
                ? projectDeleted.water_meter_project_id
                : deleteType === "user"
                ? userDeleted.user_id
                : deleteType === "admin"
                ? adminDeleted.admin_id
                : deleteType === "simpleCounter"
                ? simpleCounterDeleted.water_meter_serial
                : deleteType === "module"
                ? moduleDeleted.water_meter_module_id
                : counterConsuptionDeleted.value
            )
          }
          text={`حذف`}
          color="red"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default DeleteForm;
