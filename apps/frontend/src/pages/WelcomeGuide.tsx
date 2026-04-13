const WelcomeGuide = () => {
  return (
    <div className="mx-8 flex flex-col h-[100vh] justify-center items-start">
      {/* some text */}
      <p className="border-2 bg-gray-200 px-2 rounded-lg mb-4">
        Welcome to ICEE
      </p>
      <h1 className="text-4xl font-bold mb-6">
        BECOME A <br />
        BETTER STUDENT
      </h1>
      <p className="text-gray-400 mb-[4rem]">
        Let’s get things ready for your first study journey with us!
      </p>

      {/* section for guides with cards */}
      <div className="flex gap-2 mb-2">
        {/* 33 rem each */}
        <div
          className="w-[20rem] h-[180px] bg-gray-200 p-6 rounded-lg"
          onClick={() => {
            window.location.href = "/network-blocker";
          }}
        >
          <h1 className="text-2xl font-bold mb-6">1. Setup block app/site</h1>
          <p className="text-gray-400">
            Keep those pesky, annoying website from interrupting your study
            session.
          </p>
        </div>

        <div
          className="w-[20rem] h-[180px] bg-gray-200 p-6 rounded-lg "
          onClick={() => {
            window.location.href = "/pomodoro";
          }}
        >
          <h1 className="text-2xl font-bold mb-6">2. Pomodoro timer</h1>
          <p className="text-gray-400">
            A 25-minutes session with short break and long break spanning
            between sessions
          </p>
        </div>
      </div>

      {/* section for noticing user */}
      <div>
        <p className="text-gray-400">
          <strong className="underline cursor-pointer">
            Disable this screen
          </strong>{" "}
          if you have already familiar with the app. You can enable this screen
          later in Settings.
        </p>
      </div>
    </div>
  );
};

export default WelcomeGuide;
