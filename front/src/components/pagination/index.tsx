import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import SelectInput from "components/fields/SelectInput";
import { useState } from "react";
import { CountOption, countSelect } from "variables";

interface CustomPaginationProps {
  page: number;
  // totalPages:number;
  pageSize: CountOption;
  totalData: number;
  changeCount: React.Dispatch<any>;
  changePageFunc: React.Dispatch<any>;
}
const CustomPagination = (props: CustomPaginationProps) => {
  const {
    page: currentPage,
    // totalPages,
    pageSize,
    totalData,
    changePageFunc,
    changeCount,
  } = props;
  const [cusPage, setCusPage] = useState<number>(currentPage);
  const totalPages = totalData
    ? totalData % pageSize.value !== 0
      ? Math.floor(totalData / pageSize.value) + 1
      : Math.floor(totalData / pageSize.value)
    : 0;
  const handlePageChange = (pageNumber: number) => {
    changePageFunc(pageNumber);
  };
  const MAX_VISIBLE_PAGES = 5; // Adjust as needed
  const visiblePages = [];

  // Calculate starting and ending page numbers with edge case handling
  let startIndex = Math.max(
    Math.min(
      currentPage - Math.floor(MAX_VISIBLE_PAGES / 2),
      totalPages - MAX_VISIBLE_PAGES + 1
    ),
    1
  );
  let endIndex = Math.min(startIndex + MAX_VISIBLE_PAGES - 1, totalPages);

  // Handle cases where totalPages < MAX_VISIBLE_PAGES
  if (totalPages < MAX_VISIBLE_PAGES) {
    startIndex = 1;
    endIndex = totalPages;
  }

  // Create page numbers for visible range
  for (let i = startIndex; i <= endIndex; i++) {
    visiblePages.push(i);
  }

  // Create ellipsis elements for hidden pages
  const hasEllipsisBefore = startIndex > 2;
  const hasEllipsisAfter = endIndex < totalPages - 1;
  return (
    <>
      <div className="flex items-end justify-between  px-4 py-3 sm:px-6">
        <div className=" sm:flex sm:flex-1 sm:items-end sm:justify-between">
          <div className="pagination-btns">
            <nav className="isolate inline-flex rounded-md ">
              {hasEllipsisBefore && (
                <span
                  className="relative mx-1 inline-flex cursor-pointer items-center rounded-full  px-3 py-2  text-sm font-semibold focus:z-20 focus:outline-offset-0"
                  onClick={() => handlePageChange(1)}
                >
                  ...
                </span>
              )}
              {visiblePages.map((page) => (
                <span
                  key={page}
                  className={`relative mx-1 inline-flex cursor-pointer items-center rounded-full  px-3 py-2  text-sm font-semibold focus:z-20 focus:outline-offset-0 ${
                    page === currentPage
                      ? "bg-indigo-600 text-white focus-visible:outline-indigo-600"
                      : "hover:  text-gray-900 hover:bg-gray-100 hover:text-gray-900 dark:text-white"
                  }`}
                  onClick={() => handlePageChange(page)}
                >
                  {page}
                </span>
              ))}
              {hasEllipsisAfter && (
                <span
                  className="relative mx-1 inline-flex cursor-pointer items-center rounded-full  px-3 py-2  text-sm font-semibold focus:z-20 focus:outline-offset-0"
                  onClick={() => handlePageChange(totalPages)}
                >
                  ...
                </span>
              )}
            </nav>
          </div>
          <div className="  flex min-w-[30%] flex-row items-end justify-between space-x-2 ">
            <CustomButton
              color="brand"
              text="رفتن به صفحه"
              onClick={() => {
                changePageFunc(Number(cusPage));
              }}
              isDisabled={
                cusPage === currentPage ||
                isNaN(cusPage) ||
                cusPage > totalPages ||
                !cusPage
                  ? true
                  : false
              }
            />
            <InputField
              id="current-page"
              type="text"
              state={cusPage}
              setState={setCusPage}
              placeholder=""
              label=""
              extra="max-w-[150px]"
            />
          </div>
          <div className=" min-w-[15%]">
            <SelectInput
              //   label="تعداد نمایش"
              dynamicOptions={countSelect}
              state={pageSize}
              setState={changeCount}
              isMandatory={true}
              isCount={true}
              setPage={changePageFunc}
              setCount={changeCount}
            />
          </div>
          <div className="pagination-disc">
            <p className="text-sm text-gray-700 dark:text-white">
              نمایش داده{" "}
              <span className="font-medium">
                {(currentPage - 1) * pageSize.value + 1}
              </span>{" "}
              تا{" "}
              <span className="font-medium">
                {currentPage * pageSize.value > totalData
                  ? totalData
                  : currentPage * pageSize.value}
              </span>{" "}
              از <span className="font-medium">{totalData}</span> رکورد
            </p>
          </div>
        </div>
      </div>
    </>
  );
};
export default CustomPagination;
