import Card from "components/card";
import { MdAdd, MdDelete, MdEdit } from "react-icons/md";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import { useState } from "react";
import ModuleTypeForm from "components/forms/ModuleTypeForm";
export type ModuleTypeObject = {
  admin_info?: string;
  module_type_id: string;
  module_type_name: string;
  module_type_create_date: Date;
  module_other_information: {};
};
type ModuletypesData = Array<{
  moduleTypeName: string;
  moduleTypeCreateDate: string;
  moduleTypeActions: JSX.Element;
}>;
const Moduletypes = () => {
  const [moduleTypeName, setModuleTypeName] = useState<string>("");
  const [isEdit, setIsEdit] = useState<boolean>(false);
  const [moduleTypeId, setModuleTypeId] = useState<string>("");
  const {
    data: moduleTypesData,
    isLoading: moduleTypesIsLoading,
    status: moduleTypesStatus,
    refetch: moduleTypesRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("ModuleType/admin/getAll", {
        page: 1,
        count: 10,
        module_type_name: null,
      }),
    queryKey: ["moduleTypeList"],
  });

  const {
    isOpen: isModuleTypeOpen,
    onOpen: onModuleTypeOpen,
    onClose: onModuleTypeClose,
  } = useDisclosure();
  const editModuleTypeClicked = (id: string) => {
    setIsEdit(true);
    let selectedModule: ModuleTypeObject = moduleTypesData.data.filter(
      (moduleType: ModuleTypeObject) => moduleType.module_type_id === id
    )[0];
    setModuleTypeId(id);
    setModuleTypeName(selectedModule.module_type_name);
    onModuleTypeOpen();
  };
  const deleteModuleTypeClicked = (id: string) => {
    console.log(id);
  };
  const renderTagActions = (moduleId: string) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => editModuleTypeClicked(moduleId)}
          icon={<MdEdit />}
          color="orange"
          extra="!p-2"
        />
        <CustomButton
          onClick={() => {
            if (window.confirm("آیا از حذف این نوع ماژول اطمینان دارید؟")) {
              deleteModuleTypeClicked(moduleId)
            }
          }}
          icon={<MdDelete />}
          color="red"
          extra="!p-2"
        />
      </div>
    );
  };
  const tagsTableHeader = [
    { title: "نوع ماژول", headerKey: "moduleTypeName" },
    { title: "تاریخ ایجاد", headerKey: "moduleTypeCreateDate" },
    { title: "عملیات", headerKey: "moduleTypeActions" },
  ];
  const tableData = () => {
    let tagsTableData: ModuletypesData = [];
    if (!moduleTypesIsLoading && moduleTypesStatus === "success") {
      moduleTypesData.data?.forEach((obj: ModuleTypeObject) =>
        tagsTableData.push({
          moduleTypeName: obj.module_type_name,
          moduleTypeCreateDate: toPersianDate(obj.module_type_create_date),
          moduleTypeActions: renderTagActions(obj.module_type_id),
        })
      );
    }
    return tagsTableData;
  };
  const clearData = () => {
    setIsEdit(false);
    setModuleTypeId("");
    setModuleTypeName("");
  };
  return (
    <div className=" users-table-container">
      <CustomModal
        isOpen={isModuleTypeOpen}
        onClose={onModuleTypeClose}
        title={"نوع ماژول"}
        modalType="form"
        information={null}
        modalForm={
          <ModuleTypeForm
            moduleTypeName={moduleTypeName}
            setModuleTypeName={setModuleTypeName}
            moduleId={moduleTypeId}
            onClose={onModuleTypeClose}
            updateTable={moduleTypesRefetch}
            isEditForm={isEdit}
            clearForm={clearData}
          />
        }
      />
      <Card extra="border-none h-max">
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`نوع ماژول (${
              moduleTypesIsLoading
                ? "loading..."
                : moduleTypesData?.data?.length
            })`}
          </div>
          <div className=" moldal-btns flex items-center justify-end">
            <CustomButton
              text="ایجاد نوع ماژول"
              onClick={() => {
                clearData();
                onModuleTypeOpen();
              }}
              icon={<MdAdd />}
              color="green"
              extra="ml-4"
            />
          </div>
        </div>
        <SimpleTable
          header={tagsTableHeader}
          data={tableData()}
          hasIndex={true}
          extra="!h-[65vh]"
        />
      </Card>
      <div className="pagination my-4 py-4"></div>
    </div>
  );
};
export default Moduletypes;
