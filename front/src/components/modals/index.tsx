import { Modal, ModalOverlay, ModalContent, ModalBody } from "@chakra-ui/react";
import Card from "components/card";
interface CustomModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  modalType: "confirmation" | "form";
  information?: null | JSX.Element;
  modalForm?: null | JSX.Element;
  onSubmit?: null | Function;
  isBill?: boolean;
  isPattern?: boolean;
}
const CustomModal = (props: CustomModalProps) => {
  const {
    isOpen,
    onClose,
    title,
    modalType,
    modalForm,
    information,
    // onSubmit,
    isBill,
    isPattern,
  } = props;
  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} size={`${isBill ? "xl" : "sm"}`}>
        <ModalOverlay className="bg-[#000] !opacity-50" />
        <ModalContent
          className={`!z-[1002] !m-auto  !w-max min-w-[350px] !max-w-[85%] !overflow-auto  px-2 md:min-w-[450px] ${
            isBill ? " " : isPattern ? "!w-[55%]" : ""
          } !bg-none !shadow-none md:top-[4vh]`}
        >
          <ModalBody>
            <Card extra="!z-[1004] flex w-full flex-col px-4 pb-[35px] pt-[35px] !h-auto !overflow-auto ">
              <h1 className="mb-[20px] text-2xl font-bold">{title}</h1>

              {modalType === "form" ? (
                modalForm
              ) : (
                <p className="mb-[20px]">{information}</p>
              )}
              {modalType === "form" ? null : (
                <div className="flex justify-end gap-2">
                  <button
                    onClick={onClose}
                    className="linear rounded-xl border-2 border-red-500 px-5 py-3 text-base font-medium text-red-500 transition duration-200 hover:bg-red-600/5 active:bg-red-700/5 dark:border-red-400 dark:bg-red-400/10 dark:text-white dark:hover:bg-red-300/10 dark:active:bg-red-200/10"
                  >
                    بستن
                  </button>
                </div>
              )}
            </Card>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};
export default CustomModal;
