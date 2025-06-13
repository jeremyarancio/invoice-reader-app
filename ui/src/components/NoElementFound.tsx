import missElement from "@/assets/missElement.png";

interface Props {
    type: string;
}

function NoElementFound({ type }: Props) {
    return (
        <>
            <div className=" flex flex-col justify-center items-center space-y-4">
                <img
                    src={missElement}
                    alt="No element found"
                    className="size-32 mx-auto"
                />
                <h2>No {type} found.</h2>
            </div>
        </>
    );
}

export default NoElementFound;
