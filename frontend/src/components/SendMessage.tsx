const sendBtn = (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={1.5}
    stroke="currentColor"
    className="w-6 h-6 transform scale-125"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
    />
  </svg>
);

type Props = {
  btnStyle: string;
  text: string;
  setText: any;
  handleUserTextSent: any;
};

function SendMessage({ btnStyle, text, setText, handleUserTextSent }: Props) {
  return (
    <button
      onClick={() => {
        handleUserTextSent(text);
        setText("")
      }}
      className={btnStyle + "transform -rotate-45 hover:text-sky-600"}
    >
      {sendBtn}
    </button>
  );
}

export default SendMessage;
