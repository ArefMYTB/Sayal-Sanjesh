import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import { useEffect, useState } from "react";
import { FaTimes } from "react-icons/fa";

interface SnapshotSelectFilterProps {
  filterPage: "showSnapshot" | "createSnapshot";
  projectSelect: DynamicOption[] | null;
  counterSelect?: DynamicOption[] | null;
  project: DynamicOption | null;
  setProject: React.Dispatch<any>;
  counter?: DynamicOption | null;
  setCounter?: React.Dispatch<any>;
  serialSearch?: string;
  setSerialSearch?: React.Dispatch<React.SetStateAction<string>>;
}

const SnapshotSelectFilter = (props: SnapshotSelectFilterProps) => {
  const {
    filterPage,
    projectSelect,
    counterSelect,
    project,
    setProject,
    counter,
    setCounter,
    serialSearch,
    setSerialSearch,
  } = props;

  const [internalSearch, setInternalSearch] = useState(serialSearch ?? "");

  // debounce effect
  useEffect(() => {
    const timeout = setTimeout(() => {
      if (setSerialSearch) setSerialSearch(internalSearch);
    }, 500); // adjust debounce delay as needed
    return () => clearTimeout(timeout);
  }, [internalSearch]);

  return (
    <div
      className={`grid ${
        filterPage === "showSnapshot" ? "grid-cols-3" : "grid-cols-3"
      } gap-4`}
    >
      <SelectInput
        label="پروژه دستگاه"
        placeholder="پروژه مورد نظر را انتخاب کنید"
        dynamicOptions={projectSelect}
        state={project}
        setState={setProject}
      />
      <SelectInput
        label="نام دستگاه"
        placeholder="دستگاه مورد نظر را انتخاب کنید"
        dynamicOptions={counterSelect}
        state={counter}
        setState={setCounter}
        disabled={!project}
      />
      <div className="mx-2">
        <label className="ml-3 text-sm font-bold text-navy-700 dark:text-white">
          جستجو با شماره سریال
        </label>
        <div>
          {/* Remove button (only visible if there's text) */}
          {internalSearch && (
            <button
              type="button"
              onClick={() => setInternalSearch("")}
              className="absolute left-9 mt-3.5 text-gray-400 hover:text-gray-600 focus:outline-none"
            >
              <FaTimes />
            </button>
          )}

          <input
            type="text"
            value={internalSearch}
            onChange={(e) => setInternalSearch(e.target.value)}
            placeholder="شماره سریال را وارد کنید"
            className="mt-2 block w-full rounded-md border border-gray-300 bg-white p-[12px] text-sm focus:border-blue-400 focus:outline-none focus:ring-1 focus:ring-blue-400 dark:bg-navy-800"
          />
        </div>
      </div>
    </div>
  );
};

export default SnapshotSelectFilter;
