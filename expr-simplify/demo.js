// https://buttondown.email/jaffray/archive/simplifying-expressions-bottom-up/

const Number = (value) => ({
    type: "number",
    value,
});

const Variable = (name) => ({
    type: "variable",
    name,
});

const Plus = (left, right) => ({
    type: "plus",
    left,
    right,
});

const Minus = (left, right) => ({
    type: "minus",
    left,
    right,
});

const Times = (left, right) => ({
    type: "times",
    left,
    right,
});

function simplify(node) {
    switch (node.type) {
        case "plus": {
            const left = simplify(node.left);
            const right = simplify(node.right);

            // Commute variables to the left.
            if (left.type !== "variable" && right.type === "variable") {
                return Plus(right, left)
            }

            // Fold 0 + x => x.
            if (left.type === "number" && left.value === 0) {
                return right;
            }

            // Fold x + 0 => x.
            if (right.type === "number" && right.value === 0) {
                return left;
            }

            return Plus(left, right);
        }
        case "minus": {
            const left = simplify(node.left);
            const right = simplify(node.right);

            return Minus(left, right);
        }
        case "times": {
            const left = simplify(node.left);
            const right = simplify(node.right);

            return Times(left, right);
        }
        default:
            return node;
    }
}


let expression = Plus(Number(0), Variable("a"));
expression = simplify(expression);
console.log(expression);
