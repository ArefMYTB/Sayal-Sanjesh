import Card from "components/card";
import { MdAdd, MdDelete, MdEdit } from "react-icons/md";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import { TagObject } from "views/counters";
import DeviceTypeForm from "components/forms/DeviceTypeForm";
import { DynamicOption } from "components/fields/SelectInput";
import { useState } from "react";
import { renderToast } from "utils/globalUtils";
export type TypeObject = {
  water_meter_type_id: string;
  water_meter_type_name: string;
  water_meter_type_create_date: Date;
  water_meter_tag: TagObject;
  water_meter_type_files: string[];
  All_counter_with_this_type: number;
  All_project_with_this_type: number;
  meter_per_type: number;
};
type DeviceTypeTableData = Array<{
  typeName: string;
  typeCreateDate: string;
  tagName: JSX.Element;
  projectWithType: string;
  deviceWithType: string;
  typeActions: JSX.Element;
}>;
const DeviceTypesTable = () => {
  const [tag, setTag] = useState<DynamicOption>(null);
  const [deviceTypeName, setDeviceTypeName] = useState<string>("");
  const {
    data: typesData,
    isLoading: typesIsLoading,
    status: typesStatus,
    refetch: typesRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterTypes/admin/getAll", {
        page: 1,
        count: 20,
        water_meter_type_name: "",
        water_meter_type_create_date: "",
      }),
    queryKey: ["typesList"],
  });
  const {
    data: tagsData,
    isLoading: tagsIsLoading,
    status: tagsStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterTags/admin/getAll", {
        page: 1,
        count: 10,
        water_meter_tag_name: "",
        water_meter_type_create_date: "",
      }),
    queryKey: ["tagsList"],
  });
  const {
    isOpen: isTypesOpen,
    onOpen: onTypesOpen,
    onClose: onTypesClose,
  } = useDisclosure();
  const editProjectClick = (id: string) => {
    // //console.log(id);
    // onTypesOpen();
  };
  const deleteDeviceType = async (id: string) => {
    // //console.log(id);
    const response = await reqFunction("WaterMeterTypes/admin/delete", {
      water_meter_type_id: id,
    });
    if (response.code === 200) {
      renderToast("نوع دستگاه با موفقیت حذف شد.", "success");
      typesRefetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف نوع دستگاه مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderTypeActions = (typeId: string) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => editProjectClick(typeId)}
          icon={<MdEdit />}
          color="orange"
          extra="!p-2"
        />
        <CustomButton
          onClick={() => {
            if (window.confirm("آیا از حذف این نوع دستگاه اطمینان دارید؟")) {
              deleteDeviceType(typeId);
            }
          }}
          icon={<MdDelete />}
          color="red"
          extra="!p-2"
        />
      </div>
    );
  };
  const typesTableHeader = [
    { title: "نوع دستگاه", headerKey: "typeName" },
    { title: "دسته بندی", headerKey: "tagName" },
    { title: "تاریخ ایجاد", headerKey: "typeCreateDate" },
    { title: "تعداد پروژه", headerKey: "projectWithType" },
    { title: "تعداد دستگاه", headerKey: "deviceWithType" },
    { title: "عملیات", headerKey: "typeActions" },
  ];
  const tableData = () => {
    let typesTableData: DeviceTypeTableData = [];
    if (!typesIsLoading && typesStatus !== "pending") {
      typesData.data?.forEach((obj: TypeObject) =>
        typesTableData.push({
          typeName: obj.water_meter_type_name,
          tagName: (
            <span
              className={`${
                obj.water_meter_tag.water_meter_tag_name === "آب"
                  ? " bg-blue-500"
                  : obj.water_meter_tag.water_meter_tag_name === "برق"
                  ? " bg-red-500"
                  : obj.water_meter_tag.water_meter_tag_name === "گاز"
                  ? "bg-orange-600"
                  : " bg-yellow-600"
              } rounded px-2 text-sm text-white`}
            >
              {obj.water_meter_tag.water_meter_tag_name}
            </span>
          ),
          typeCreateDate: toPersianDate(obj.water_meter_type_create_date),
          projectWithType: `${obj.All_project_with_this_type} عدد`,
          deviceWithType: `${obj.All_counter_with_this_type} عدد`,
          typeActions: renderTypeActions(obj.water_meter_type_id),
        })
      );
    }
    return typesTableData;
  };
  const renderTagSelectData = () => {
    let selectData: DynamicOption[] = [];
    if (!tagsIsLoading && tagsStatus !== "pending") {
      tagsData.data.forEach((tag: TagObject) =>
        selectData.push({
          label: tag.water_meter_tag_name,
          value: tag.water_meter_tag_id,
        })
      );
    }
    return selectData;
  };
  return (
    <div className=" users-table-container">
      <CustomModal
        isOpen={isTypesOpen}
        onClose={onTypesClose}
        title={"نوع دستگاه"}
        modalType="form"
        information={null}
        modalForm={
          <DeviceTypeForm
            tagSelectData={renderTagSelectData()}
            tag={tag}
            setTag={setTag}
            deviceTypeName={deviceTypeName}
            setDeviceTypeName={setDeviceTypeName}
            onClose={onTypesClose}
            updateTable={typesRefetch}
          />
        }
      />
      <Card extra="border-none h-max">
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`انواع دستگاه (${
              typesIsLoading ? "loading..." : typesData?.data?.length
            })`}
          </div>
          <div className=" moldal-btns flex items-center justify-end">
            <CustomButton
              text="ایجاد نوع دستگاه"
              onClick={onTypesOpen}
              icon={<MdAdd />}
              color="green"
              extra="ml-4"
            />
          </div>
        </div>
        <SimpleTable
          header={typesTableHeader}
          data={tableData()}
          hasIndex={true}
          extra="!h-[65vh]"
        />
      </Card>
      <div className="pagination my-4 py-4"></div>
    </div>
  );
};
export default DeviceTypesTable;
