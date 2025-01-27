import SelectInput, { DynamicOption } from "components/fields/SelectInput";
// import { useState } from "react";

interface ProjectSettingsFilterProps {
  filterPage: "projectPattern" | "other";
  projectSelect: DynamicOption[] | null;
  tagSelect: DynamicOption[] | null;
  project: DynamicOption | null;
  setProject: React.Dispatch<any>;
  tag: DynamicOption | null;
  setTag: React.Dispatch<any>;
}
const ProjectSettingsFilter = (props: ProjectSettingsFilterProps) => {
  const {
    filterPage,
    projectSelect,
    tagSelect,
    project,
    setProject,
    tag,
    setTag,
  } = props;

  return (
    <div
      className={`grid ${
        filterPage === "projectPattern" ? "grid-cols-2" : "grid-cols-3"
      } `}
    >
      <SelectInput
        label=" پروژه دستگاه"
        placeholder="پروژه مورد نظر را انتخاب کنید"
        dynamicOptions={projectSelect}
        state={project}
        setState={setProject}
        disabled={tag ? true : false}
      />
      <SelectInput
        label="دسته بندی"
        placeholder="دسته بندی مورد نظر را انتخاب کنید"
        dynamicOptions={tagSelect}
        state={tag}
        setState={setTag}
      />
    </div>
  );
};
export default ProjectSettingsFilter;
