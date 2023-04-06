const midi = require("midi");

const findLaunchpad = () => {
  const output = new midi.Output();
  const portCount = output.getPortCount();

  for (let i = 0; i < portCount; i++) {
    const portName = output.getPortName(i);
    if (portName.includes("Launchpad")) {
      return i;
    }
  }

  return null;
};

const main = () => {
  const outputPortIndex = findLaunchpad();

  if (outputPortIndex === null) {
    console.error("Error: Launchpad not found.");
    process.exit(1);
  }

  const output = new midi.Output();
  output.openPort(outputPortIndex);

  const x = 2;
  const y = 1;
  const red = 62;
  const green = 62;
  const blue = 62;

  const button = 11;
  const sysexMessage = [
    240,
    0,
    32,
    41,
    2,
    24,
    11,
    button,
    red,
    green,
    blue,
    247,
  ];
  output.sendMessage(sysexMessage);

  setTimeout(() => {
    output.closePort();
  }, 5000); // Keep the LED lit for 5 seconds
};

main();
