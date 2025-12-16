// frontend/jest.config.js

/*
Next.js で Jest を使ってテストするなら
必須に近い Jest の設定ファイル



frontend のテストは
本物のブラウザで動作せず
ブラウザっぽい環境で動かす

そのための Jest の設定ファイル
*/



/*
next/jest を使う

JS/TS の変換
CSS
設定読み込みなど
Next.js の事情を

Jest に合わせる接着剤
*/
const nextJest = require("next/jest");

const createJestConfig = nextJest({ dir: "./" });



// /** */ はJSDoc として解釈され、エディタや TypeScript が意味のあるコメントとして扱う
/** @type {import('jest').Config} */
const customJestConfig =
{
    /*
    テストをブラウザっぽく動かす
    DOM がある前提のテストが動く
    */
    testEnvironment: "jsdom",

    /*
    テスト開始前に、毎回読み込む準備ファイルを指定
    @testing-library/jest-dom を有効化する場所
    */
    setupFilesAfterEnv: ["<rootDir>/jest.setup.ts"],

    /*
    テスト中に
    import "./x.module.css" とか
    import img from "./a.png" が来ると、Jest は詰む

    なので
    「CSS はダミー扱い」
    「画像もダミー扱い」にしてテストを継続させる。
    */
    moduleNameMapper:
    {
        "^.+\\.module\\.(css|sass|scss)$": "identity-obj-proxy",
        "^.+\\.(png|jpg|jpeg|gif|webp|svg)$": "<rootDir>/__mocks__/fileMock.js",
    },
};



module.exports = createJestConfig(customJestConfig);
