import {
  Box,
  Step,
  StepDescription,
  StepIcon,
  StepIndicator,
  StepNumber,
  StepSeparator,
  StepStatus,
  StepTitle,
  Stepper,
  useSteps,
} from "@chakra-ui/react";
import CustomButton from "components/button";
type StepData = {
  step: number;
  content: JSX.Element;
};
type StepInfo = {
  title: string;
  description: string;
};
interface CustomStepperProps {
  steps: StepInfo[];
  contents: StepData[];
}
const CustomStepper = (props: CustomStepperProps) => {
  const { steps, contents } = props;
  const { activeStep, setActiveStep, goToNext, goToPrevious } = useSteps({
    index: 0,
    count: steps.length,
  });
  const renderContents = () => {
    if (activeStep === steps.length) {
      return contents.filter((content) => content.step === activeStep - 1)[0];
    } else {
      return contents.filter((content) => content.step === activeStep)[0];
    }
  };
  return (
    <div className="h-full dark:text-white">
      <div className="stepper py-4">
        <Stepper size="lg" index={activeStep}>
          {steps.map((step, index) => (
            <Step key={index} onClick={() => setActiveStep(index)}>
              <StepIndicator>
                <StepStatus
                  complete={<StepIcon />}
                  incomplete={<StepNumber />}
                  active={<StepNumber />}
                />
              </StepIndicator>

              <Box flexShrink="0">
                <StepTitle>{step.title}</StepTitle>
                <StepDescription>{step.description}</StepDescription>
              </Box>

              <StepSeparator />
            </Step>
          ))}
        </Stepper>
      </div>
      <div className="steps-content py 4">
        {renderContents().content.props.children}
      </div>
      <div className="step-btns flex items-center justify-between py-4">
        <CustomButton
          onClick={() => goToPrevious()}
          text="مرحله قبل"
          color="brand"
          isDisabled={activeStep === 0}
        />
        <CustomButton
          onClick={() => goToNext()}
          text={activeStep === steps.length ? "تایید فرم" : "مرحله بعد"}
          color="brand"
        />
      </div>
    </div>
  );
};
export default CustomStepper;
