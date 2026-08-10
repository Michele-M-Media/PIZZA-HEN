/* PIZZA HEN KStuff Selector - websrv homebrew.js extension
 * Uses the upstream websrv extension API with exactly two manual choices.
 */
async function main() {
    const ACTION = "/data/PIZZA_HEN/bin/pizzahen-kstuff-select.elf";
    const ICON = "/fs/data/PIZZA_HEN/pizzahen.png";

    const items = [
        {
            mainText: "KStuff Lite 1.09",
            secondaryText: "EchoStretch - Modern Mode",
            imgPath: ICON,
            onclick: async () => ({ path: ACTION, args: ["lite"], daemon: true })
        },
        {
            mainText: "KStuff DR 1.2",
            secondaryText: "Drakmor - Compatibility Mode",
            imgPath: ICON,
            onclick: async () => ({ path: ACTION, args: ["dr"], daemon: true })
        }
    ];

    const openSelector = async () => {
        showCarousel(items);
        return null;
    };

    // The extension is loaded while websrv renders its home page. Delay the
    // navigation slightly so the selector becomes the foreground carousel.
    setTimeout(() => showCarousel(items), 450);

    return {
        mainText: "PIZZA HEN",
        secondaryText: "KStuff Engine Selector",
        imgPath: ICON,
        onclick: openSelector
    };
}
