import { useDisclosure } from "@chakra-ui/hooks";
import { useQuery } from "@tanstack/react-query";
import CustomButton from "components/button";
import { DynamicOption } from "components/fields/SelectInput";
import DeleteForm from "components/forms/DeleteForm";
import ModuleForm from "components/forms/ModuleForm";
import Loading from "components/loading";
import CustomModal from "components/modals";
import CustomPagination from "components/pagination";
import SimpleTable from "components/tables/SimpleTable";
import { useState } from "react";
import { MdDelete, MdEdit } from "react-icons/md";
import { reqFunction } from "utils/API";
import { renderModuleAttr, renderToast } from "utils/globalUtils";
import { CountOption, countSelect, simOprators } from "variables";
import { ModuleTypeObject } from "views/settings/ModuleTypesTable";
export type ModuleObject = {
  admin_info: {
    admin_id: string;
    admin_name: string;
    admin_lastname: string;
    admin_phone: string;
  };
  module_type_info: ModuleTypeObject;
  modules_total_number: number;
  water_meter_module_code: string;
  water_meter_module_create_date: string;
  water_meter_module_id: string;
  water_meter_module_name: string;
  water_meter_module_other_information: {};
  water_meter_module_property: string[];
  water_meter_module_sim: string;
  water_meter_module_sim_operator: string;
  water_meter_module_unit: null;
};
type ModuleTableData = {
  moduleName: string;
  moduleType: string;
  moduleCode: string;
  moduleProperties: JSX.Element;
  moduleSimOperator: string;
  moduleSim: string;
  moduleActions: JSX.Element;
};
const ModuleStorage = () => {
  const [selectedModule, setSelectedModule] = useState<ModuleObject | null>(
    null
  );
  const [isEdit, setIsEdit] = useState<boolean>(false);
  const [page, setPage] = useState<number>(1);
  const [count, setCount] = useState<CountOption>(countSelect?.[0]);
  const {
    data: moduleTypesData,
    isLoading: moduleTypesIsLoading,
    status: moduleTypesStatus,
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
    data: modulesData,
    isLoading: modulesIsLoading,
    status: modulesStatus,
    refetch: moduleRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterModules/admin/getAll", {
        page: page,
        count: count.value,
        water_meter_module_name: "",
        water_meter_module_create_date: "",
        mood: "modules_without_meter",
      }),
    queryKey: ["modulesList", page, count],
  });
  const {
    isOpen: isAddModuleOpen,
    onOpen: onAddModuleOpen,
    onClose: onAddModuleClose,
  } = useDisclosure();
  const {
    isOpen: isDeleteConfirmOpen,
    onOpen: onDeleteConfirmOpen,
    onClose: onDeletConfirmClose,
  } = useDisclosure();
  const tableHeader = [
    { title: "نام ماژول", headerKey: "moduleName" },
    { title: "نوع ماژول", headerKey: "moduleType" },
    { title: "کد ماژول", headerKey: "moduleCode" },
    { title: "ویژگی های ماژول", headerKey: "moduleProperties" },
    { title: "اپراتور سیمکارت", headerKey: "moduleSimOperator" },
    { title: "شماره سیمکارت", headerKey: "moduleSim" },
    { title: "عملیات", headerKey: "moduleActions" },
  ];
  const editModuleClick = (object: ModuleObject) => {
    setSelectedModule(object);
    setIsEdit(true);
    onAddModuleOpen();
  };
  const deleteModuleClicked = (object: ModuleObject) => {
    setSelectedModule(object);
    onDeleteConfirmOpen();
  };
  const deleteModule = async (ModuleId: string) => {
    const response = await reqFunction("WaterMeterModules/admin/delete", {
      water_meter_module_id: ModuleId,
    });
    if (response.code === 200) {
      renderToast("ماژول با موفقیت حذف شد.", "success");
      onDeletConfirmClose();
      setSelectedModule(null);
      moduleRefetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف ماژول مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderModuleActions = (moduleObject: ModuleObject) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => editModuleClick(moduleObject)}
          icon={<MdEdit />}
          color="orange"
          extra="!p-2"
        />
        <CustomButton
          onClick={() => {
            if (window.confirm("آیا از حذف این ماژول اطمینان دارید؟")) {
              deleteModuleClicked(moduleObject)
            }
          }}
          icon={<MdDelete />}
          color="red"
          extra="!p-2"
        />
      </div>
    );
  };
  const renderModuleTypes = () => {
    let allTypes: ModuleTypeObject[] = moduleTypesData?.data
      ? moduleTypesData.data
      : [];
    let selectData: DynamicOption[] = [];
    allTypes?.forEach((type) =>
      selectData.push({
        label: type.module_type_name,
        value: type.module_type_id,
      })
    );
    return selectData;
  };
  const tableData = () => {
    let moduleTableData: ModuleTableData[] = [];
    modulesData.data?.forEach((eModule: ModuleObject) => {
      moduleTableData.push({
        moduleName: eModule.water_meter_module_name,
        moduleCode: eModule.water_meter_module_code,
        moduleType: eModule.module_type_info?.module_type_name
          ? eModule.module_type_info.module_type_name
          : "__",
        moduleProperties: renderModuleAttr(
          eModule.water_meter_module_property,
          eModule.water_meter_module_code
        ),
        moduleSimOperator: eModule.water_meter_module_sim_operator
          ? simOprators.filter(
              (op) => op.value === eModule.water_meter_module_sim_operator
            )[0].label
          : "__",
        moduleSim: eModule.water_meter_module_sim
          ? eModule.water_meter_module_sim
          : "__",
        moduleActions: renderModuleActions(eModule),
      });
    });

    return moduleTableData;
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
            deleteType="module"
            moduleDeleted={selectedModule}
            onClose={onDeletConfirmClose}
            deleteFunction={deleteModule}
          />
        }
      />
      <CustomModal
        title="ماژول"
        isOpen={isAddModuleOpen}
        onClose={onAddModuleClose}
        modalType="form"
        modalForm={
          <ModuleForm
            moduleInfo={selectedModule}
            setModuleInfo={setSelectedModule}
            moduleTypeSelectData={renderModuleTypes()}
            isEdit={isEdit}
            setIsEdit={setIsEdit}
            onClose={onAddModuleClose}
            updateTable={moduleRefetch}
          />
        }
      />
      <div className="relative flex items-center justify-between p-4">
        <div className="text-xl font-bold text-navy-700 dark:text-white">
          {`ماژول ها (${
            !modulesIsLoading &&
            modulesStatus === "success" &&
            modulesData.data?.[0]?.modules_total_number
              ? modulesData.data?.[0].modules_total_number
              : 0
          })`}
        </div>
        <div className=" moldal-btns flex items-center justify-end">
          <CustomButton
            text="افزودن ماژول"
            onClick={() => onAddModuleOpen()}
            icon={<></>}
            color="green"
            extra="ml-0"
          />
        </div>
      </div>
      {!modulesIsLoading &&
      modulesStatus === "success" &&
      !moduleTypesIsLoading &&
      moduleTypesStatus === "success" ? (
        <SimpleTable
          header={tableHeader}
          data={tableData()}
          extra="h-[56vh] "
          hasIndex={true}
        />
      ) : (
        <Loading />
      )}
      <div className="pagination ">
        <CustomPagination
          page={page}
          pageSize={count}
          totalData={
            !modulesIsLoading &&
            modulesStatus === "success" &&
            modulesData?.data?.length > 0
              ? modulesData.data?.[0].modules_total_number
              : 100
          }
          changePageFunc={setPage}
          changeCount={setCount}
        />
      </div>
    </>
  );
};
export default ModuleStorage;
