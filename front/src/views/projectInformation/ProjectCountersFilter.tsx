import SelectInput, { DynamicOption } from "components/fields/SelectInput";

interface ProjectCountersFilterProps {
  tagSelect: DynamicOption[] | null;
  sortValueSelect: DynamicOption[] | null;
  reversedSelect: DynamicOption[] | null;
  countSelect: DynamicOption[] | null;
  sortValue: DynamicOption | null;
  setSortValue: React.Dispatch<any>;
  tag: DynamicOption | null;
  setTag: React.Dispatch<any>;
  reversed: DynamicOption | null;
  setReversed: React.Dispatch<any>;
  // count: DynamicOption | null;
  // setCount: React.Dispatch<any>;
}
const ProjectCountersFilter = (props: ProjectCountersFilterProps) => {
  const {
    sortValueSelect,
    tagSelect,
    reversedSelect,
    // countSelect,
    sortValue,
    setSortValue,
    tag,
    setTag,
    reversed,
    setReversed,
    // count,
    // setCount,
  } = props;

  return (
    <div className={`grid grid-cols-1 gap-4 md:grid-cols-3  `}>
      <SelectInput
        label="دسته بندی"
        placeholder="دسته بندی مورد نظر را انتخاب کنید"
        dynamicOptions={tagSelect}
        state={tag}
        setState={setTag}
        isMandatory={true}
      />
      <SelectInput
        label="اولویت نمایش"
        placeholder="اولویت نمایش را انتخاب کنید"
        dynamicOptions={sortValueSelect}
        state={sortValue}
        setState={setSortValue}
        isMandatory={true}
      />

      <SelectInput
        label="نحوه نمایش"
        placeholder="نحوه نمایش مورد نظر را انتخاب کنید"
        dynamicOptions={reversedSelect}
        state={reversed}
        setState={setReversed}
        isMandatory={true}
      />
      {/* <SelectInput
        label="تعداد نمایش"
        placeholder="تعداد نمایش را انتخاب کنید"
        dynamicOptions={countSelect}
        state={count}
        setState={setCount}
        isMandatory={true}
      /> */}
    </div>
  );
};
export default ProjectCountersFilter;
