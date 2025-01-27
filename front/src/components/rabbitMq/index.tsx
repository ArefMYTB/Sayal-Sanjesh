import { useEffect, useRef } from "react";
import { Connection } from "rabbitmq-client";

const RabbitMqComponent = () => {
  const rabbitRef = useRef<Connection | undefined>(undefined);

  useEffect(() => {
    const connectToRabbitMQ = async () => {
      try {
        // Initialize RabbitMQ connection
        rabbitRef.current = new Connection(
          "amqp://guest:guest@185.94.96.200:5672"
        );

        // Listen for connection errors
        rabbitRef.current.on("error", (err) => {
          //console.log("RabbitMQ connection error", err);
        });

        // Listen for successful connection
        rabbitRef.current.on("connection", () => {
          //console.log("Connection successfully (re)established");
        });

        // Clean up when you receive a shutdown signal
        const onShutdown = async () => {
          // Close the RabbitMQ connection
          await rabbitRef.current?.close();
        };

        process.on("SIGINT", onShutdown);
        process.on("SIGTERM", onShutdown);
      } catch (error) {
        console.error("Error connecting to RabbitMQ:", error);
      }
    };

    connectToRabbitMQ();

    // Clean up function
    return () => {
      // Clean up RabbitMQ connection if component unmounts
      // Close RabbitMQ connection
      //console.log("Cleaning up RabbitMQ connection");
      // Close the RabbitMQ connection
      rabbitRef.current?.close();
    };
  }, []);

  return <></>;
};

export default RabbitMqComponent;
