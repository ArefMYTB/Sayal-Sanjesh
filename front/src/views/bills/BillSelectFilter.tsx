import SelectInput, { DynamicOption } from "components/fields/SelectInput";
// import { useState } from "react";

interface BillSelectFilterProps {
  filterPage: "showBill" | "createBill";
  projectSelect: DynamicOption[] | null;
  tagSelect: DynamicOption[] | null;
  project: DynamicOption | null;
  setProject: React.Dispatch<any>;
  tag: DynamicOption | null;
  setTag: React.Dispatch<any>;
  counter?: DynamicOption | null;
  setCounter?: React.Dispatch<any>;
  counterSelect?: DynamicOption[] | null;
}
const BillSelectFilter = (props: BillSelectFilterProps) => {
  const {
    filterPage,
    projectSelect,
    tagSelect,
    project,
    setProject,
    tag,
    setTag,
    counterSelect,
    counter,
    setCounter,
  } = props;

  return (
    <div
      className={`grid ${
        filterPage === "showBill" ? "grid-cols-3" : "grid-cols-2"
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
        disabled={project && !counter ? false : true}
      />
      {filterPage === "showBill" ? (
        <SelectInput
          label="نام دستگاه"
          placeholder="دستگاه مورد نظر را انتخاب کنید"
          dynamicOptions={counterSelect}
          state={counter}
          setState={setCounter}
          disabled={tag ? false : true}
        />
      ) : null}
    </div>
  );
};
export default BillSelectFilter;
