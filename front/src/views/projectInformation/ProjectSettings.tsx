import { ProjectObject } from "views/projects";
import ProjectSettingsFilter from "./ProjectSettingFilter";
import { DynamicOption } from "components/fields/SelectInput";
import { TagObject } from "views/counters";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import CustomButton from "components/button";
import { MdAdd, MdDelete, MdEdit } from "react-icons/md";
import CustomModal from "components/modals";
import { useDisclosure } from "@chakra-ui/hooks";
import PatternFrom from "components/forms/PatternForm";
import { renderUnit } from "utils/CommonFunctions";
import { title } from "process";
import { renderToast } from "utils/globalUtils";
// import { useParams } from "react-router-dom";
type PatternTableData = {
  fromValue: string;
  toValue: string;
  unitPrice: string;
  Delete: JSX.Element;
};
export type PatternObject = {
  all_pattern_number: number;
  pattern_id: string;
  pattern_list: { k: string; v1: string; v2: string }[];
  pattern_project: ProjectObject;
  pattern_tag: TagObject;
};
interface ProjectSettingsProps {
  // projectData?: [ProjectObject];
  // inProject: boolean;
}
const ProjectSettings = (props: ProjectSettingsProps) => {
  // const { inProject } = props;
  // const { projectId } = useParams();
  // const projectInfo = projectData[0];
  const [project, setProject] = useState<DynamicOption>(null);
  const [tag, setTag] = useState<DynamicOption>(null);
  const [patternFromValue, setPatternFromValue] = useState<string>("");
  const [patternToValue, setPatternToValue] = useState<string>("");
  const [patternUnitPrice, setPatternUnitPrice] = useState<string>("");
  const [isEditForm, setIsEditForm] = useState<boolean>(false);
  const [patternId, setPatternId] = useState<string>("");
  const [selectedPatternList, setSelectedPatternList] = useState<
    { k: string; v1: string; v2: string }[]
  >([]);
  const renderProjectSelectData = () => {
    const projectSelected: DynamicOption[] = [];
    projectData?.data?.forEach((project: ProjectObject) =>
      projectSelected.push({
        label: project.water_meter_project_name,
        value: project.water_meter_project_id,
      })
    );
    return projectSelected;
  };
  const renderTagSelectData = () => {
    const tagSelectOptins: DynamicOption[] = [];
    if (project) {
      let select: ProjectObject[] = projectData.data.filter(
        (p: ProjectObject) => project.value === p.water_meter_project_id
      );
      let tags: string[] = [];
      select[0].types.forEach((type) => {
        if (!tags.includes(type.water_meter_tag.water_meter_tag_name)) {
          tags.push(type.water_meter_tag.water_meter_tag_name);
          tagSelectOptins.push({
            value: type.water_meter_tag.water_meter_tag_id,
            label: type.water_meter_tag.water_meter_tag_name,
          });
        }
      });
    }

    return tagSelectOptins;
  };
  const {
    data: projectData,
    isLoading: projectIsLoading,
    status: projectStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterProjectsURL/admin/getAll", {
        page: 1,
        count: 100,
        water_meter_project_name: null,
        water_meter_project_create_date: null,
        user_id: null,
      }),
    queryKey: ["projectList"],
  });
  const {
    data: patternData,
    isLoading: patternIsLoading,
    status: patternStatus,
    refetch: patternRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("Pattern/admin/getAll", {
        page: 1,
        count: 10,
        project_id: project ? project.value : null,
        tag_id: tag.value,
      }),
    queryKey: ["patternList", tag, project],
  });

  const {
    isOpen: isPatternOpen,
    onOpen: onPatternOpen,
    onClose: onPatternClose,
  } = useDisclosure();
  const patternTableheader = [
    {
      title: ` از (${renderUnit(tag?.label, true)})`,
      headerKey: "fromValue",
    },
    {
      title: ` تا (${renderUnit(tag?.label, true)})`,
      headerKey: "toValue",
    },
    {
      title: `قیمت هر ${renderUnit(tag?.label, true)} (ریال)`,
      headerKey: "unitPrice",
    },
    {
      title: "حذف",
      headerKey: "Delete",
    },
  ];
  const renderPatternData = () => {
    let patternTableData: PatternTableData[] = [];
    const data: PatternObject | null =
      Array.isArray(patternData?.data) && patternData.data.length > 0
        ? patternData.data[0]
        : null;

    const patternList = data?.pattern_list;
    patternList && patternList?.length > 0
      ? patternList?.forEach((pattern) =>
          patternTableData.push({
            fromValue: pattern.v1,
            toValue: pattern.v2,
            unitPrice: pattern.k,
            Delete: renderPatternAction({
              ...pattern,
              pattern_id: data.pattern_id,
            }),
          })
        )
      : (patternTableData = []);
    return patternTableData;
  };

  const renderPatternAction = (pattern: { pattern_id: string }) => {
    return (
      <div className="flex items-center justify-center">
        <CustomButton
          onClick={() => {
            if (window.confirm("آیا از حذف این الگو اطمینان دارید؟")) {
              deletePattern(pattern);
            }
          }}
          icon={<MdDelete />}
          color="red"
          extra="!p-2"
        />
      </div>
    );
  };

  const createPattern = () => {
    setPatternId("");
    setSelectedPatternList([]);
    onPatternOpen();
    setIsEditForm(false);
  };
  const editPattern = () => {
    setPatternId(patternData.data[0].pattern_id);
    setSelectedPatternList(patternData.data[0].pattern_list);
    onPatternOpen();
    setIsEditForm(true);
  };
  const deletePattern = async (pattern: any) => {
    const response = await reqFunction("Pattern/admin/delete", {
      pattern_id: pattern.pattern_id,
    });
    if (response.code === 200) {
      renderToast("الگو با موفقیت حذف شد.", "success");
      patternRefetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف الگو مشکلی رخ داده",
        "err"
      );
    }
  };
  return (
    <div className=" py-4">
      {!projectIsLoading && projectStatus === "success" ? (
        <>
          <ProjectSettingsFilter
            filterPage="projectPattern"
            projectSelect={renderProjectSelectData()}
            tagSelect={renderTagSelectData()}
            project={project}
            setProject={setProject}
            tag={tag}
            setTag={setTag}
          />
          <CustomModal
            isOpen={isPatternOpen}
            onClose={onPatternClose}
            title={"الگو"}
            modalType="form"
            information={null}
            isPattern={isEditForm ? true : false}
            modalForm={
              <PatternFrom
                patternFromValue={patternFromValue}
                setPatternFromValue={setPatternFromValue}
                patternToValue={patternToValue}
                setPatternToValue={setPatternToValue}
                patternUnitPrice={patternUnitPrice}
                setPatternUnitPrice={setPatternUnitPrice}
                isEditForm={isEditForm}
                tag={tag}
                patternId={patternId}
                onClose={onPatternClose}
                patternList={selectedPatternList}
                setPatternList={setSelectedPatternList}
                updateTable={patternRefetch}
                projectId={project ? project.value : ""}
              />
            }
          />
        </>
      ) : (
        <></>
      )}
      {tag && !patternIsLoading && patternStatus === "success" ? (
        <>
          <div className="relative flex items-center justify-between p-4">
            <div className="text-xl font-bold text-navy-700 dark:text-white">
              الگوی مصرف
            </div>
            <div className=" moldal-btns flex items-center justify-end">
              <CustomButton
                text="افزودن الگوی مصرف"
                onClick={() => createPattern()}
                icon={<MdAdd />}
                color="green"
                extra="ml-4"
                isDisabled={patternData?.data?.length > 0 ? true : false}
              />
              <CustomButton
                text="تغییرات الگوی مصرف"
                onClick={() => editPattern()}
                icon={<MdEdit />}
                color="blue"
                extra="!ml-0"
                isDisabled={patternData?.data?.length > 0 ? false : true}
              />
            </div>
          </div>
          <SimpleTable header={patternTableheader} data={renderPatternData()} />
        </>
      ) : (
        <div className="py-2  text-navy-700  dark:text-white">
          دسته را انتخاب کنید !!!
        </div>
      )}
    </div>
  );
};
export default ProjectSettings;
