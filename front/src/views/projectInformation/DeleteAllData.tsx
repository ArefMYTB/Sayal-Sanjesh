import { useDisclosure } from "@chakra-ui/hooks";
import CustomButton from "components/button";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import DeleteForm from "components/forms/DeleteForm";
import CustomModal from "components/modals";
import { useState } from "react";
import { reqFunction } from "utils/API";
import { renderSelectData } from "utils/CommonFunctions";
import { renderToast } from "utils/globalUtils";
import { counterTagSelect } from "variables";
import { DeviceObj } from "views/counters";

interface DeleteAllDataProps {
  projectId: string;
  projectDevices: DeviceObj[];
}
const DeleteAllData = (props: DeleteAllDataProps) => {
  const { projectId, projectDevices } = props;
  const [tag, setTag] = useState<DynamicOption>(counterTagSelect[0]);
  const [device, setDevice] = useState<DynamicOption>(null);
  const {
    isOpen: isDeleteConfirmOpen,
    onOpen: onDeleteConfirmOpen,
    onClose: onDeletConfirmClose,
  } = useDisclosure();
  const deviceInTag = (tag: DynamicOption) => {
    let devicesPerTag = projectDevices.filter(
      (device) =>
        device.water_meter_type__water_meter_tag__water_meter_tag_id ===
        tag.value
    );
    return devicesPerTag;
  };
  const deleteAllConsumption = async (serial: string) => {
    // console.log(id);
    const response = await reqFunction("watermeters/admin/delete/consumption", {
      mode: "all",
      time: null,
      consumption_id: null,
      water_meter_serial: serial,
    });
    if (response.code === 200) {
      renderToast("مقادیر مصرف با موفقیت حذف شد.", "success");
      onDeletConfirmClose();
      //   usersRefetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف مقادیر مصرف مشکلی رخ داده",
        "err"
      );
    }
  };
  return (
    <>
      <CustomModal
        isOpen={isDeleteConfirmOpen}
        onClose={onDeletConfirmClose}
        title={""}
        modalType="form"
        information={null}
        modalForm={
          <DeleteForm
            deleteType="consumptions"
            counterConsuptionDeleted={device}
            onClose={onDeletConfirmClose}
            deleteFunction={deleteAllConsumption}
          />
        }
      />
      <div className="min-w-52 py-4 text-xl font-bold text-navy-700 dark:text-white">
        حذف مصارف کنتور
      </div>
      <div className={`grid grid-cols-1 gap-4 md:grid-cols-3  `}>
        <SelectInput
          label="دسته بندی"
          placeholder="دسته بندی مورد نظر را انتخاب کنید"
          dynamicOptions={counterTagSelect}
          state={tag}
          setState={setTag}
          isMandatory={true}
        />
        <SelectInput
          label="کنتور"
          placeholder="کنتور مورد نظر را انتخاب کنید"
          dynamicOptions={renderSelectData(deviceInTag(tag), "counter")}
          state={device}
          setState={setDevice}
          // isMandatory={true}
        />
        <CustomButton
          text="حذف مصرف"
          color="brand"
          onClick={() => onDeleteConfirmOpen()}
          isDisabled={device ? false : true}
          extra="max-h-[40px] self-end justify-self-start"
        />
      </div>
    </>
  );
};
export default DeleteAllData;
