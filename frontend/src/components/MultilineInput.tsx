

type Props = {
  text: string;
  setText: any;
  handleUserTextSent: any
}

const MultilineInput: React.FC<Props> = ( {text, setText, handleUserTextSent}) => {
  

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && e.shiftKey) {
      // If Shift + Enter is pressed, allow the default behavior (new line)
      return;
    } else if (e.key === 'Enter') {
      // If only Enter is pressed, prevent the default behavior
      e.preventDefault();
      // Here, you can handle the submission or any other behavior you want
      console.log(text);
      handleUserTextSent(text)
      setText("")
    }
  };

  return (
    <textarea
      placeholder="If you're done talking, you could use some typing"
      className="bg-transparent h-full w-full px-2 py-3 resize-none focus:outline-none placeholder:italic text-gray-300" 
      value={text}
      onChange={(e) => setText(e.target.value)}
      onKeyDown={handleKeyDown}
    />
  );
};

export default MultilineInput;