{*******************************************************************************
 * AllToolkit - Delphi JSON Utilities
 * 
 * 一个零依赖的 JSON 处理工具库，仅使用 Delphi 标准库。
 * 支持 JSON 的解析、生成、验证和操作。
 * 
 * 版本: 1.0.0
 * 作者: AllToolkit Contributors
 * 许可证: MIT
 *******************************************************************************}

unit JsonUtils;

interface

uses
  SysUtils, Classes, Variants;

type
  { JSON 值类型 }
  TJsonValueType = (
    jvNull,
    jvBoolean,
    jvNumber,
    jvString,
    jvArray,
    jvObject
  );

  { 前向声明 }
  TJsonValue = class;
  TJsonArray = class;
  TJsonObject = class;

  { JSON 值基类 }
  TJsonValue = class(TObject)
  private
    FValueType: TJsonValueType;
    FStringValue: string;
    FNumberValue: Double;
    FBooleanValue: Boolean;
    FArrayValue: TJsonArray;
    FObjectValue: TJsonObject;
  protected
    procedure SetValueType(AValueType: TJsonValueType);
  public
    constructor Create;
    destructor Destroy; override;
    
    { 类型检查 }
    function IsNull: Boolean;
    function IsBoolean: Boolean;
    function IsNumber: Boolean;
    function IsString: Boolean;
    function IsArray: Boolean;
    function IsObject: Boolean;
    
    { 类型转换 }
    function AsString: string;
    function AsInteger: Integer;
    function AsInt64: Int64;
    function AsDouble: Double;
    function AsBoolean: Boolean;
    function AsArray: TJsonArray;
    function AsObject: TJsonObject;
    
    { 获取值（带默认值）}
    function GetString(const DefaultValue: string = ''): string;
    function GetInteger(DefaultValue: Integer = 0): Integer;
    function GetInt64(DefaultValue: Int64 = 0): Int64;
    function GetDouble(DefaultValue: Double = 0.0): Double;
    function GetBoolean(DefaultValue: Boolean = False): Boolean;
    
    { 设置值 }
    procedure SetNull;
    procedure SetString(const AValue: string);
    procedure SetInteger(AValue: Integer);
    procedure SetInt64(AValue: Int64);
    procedure SetDouble(AValue: Double);
    procedure SetBoolean(AValue: Boolean);
    procedure SetArray(AArray: TJsonArray);
    procedure SetObject(AObject: TJsonObject);
    
    { 序列化 }
    function ToJson: string;
    function ToPrettyJson(Indent: string = '  '): string;
    
    property ValueType: TJsonValueType read FValueType;
    property StringValue: string read FStringValue write SetString;
    property NumberValue: Double read FNumberValue write SetDouble;
    property BooleanValue: Boolean read FBooleanValue write SetBoolean;
  end;

  { JSON 数组类 }
  TJsonArray = class(TObject)
  private
    FItems: TList;
    function GetCount: Integer;
    function GetItem(Index: Integer): TJsonValue;
  public
    constructor Create;
    destructor Destroy; override;
    
    { 添加元素 }
    procedure AddNull;
    procedure AddString(const AValue: string);
    procedure AddInteger(AValue: Integer);
    procedure AddInt64(AValue: Int64);
    procedure AddDouble(AValue: Double);
    procedure AddBoolean(AValue: Boolean);
    function AddArray: TJsonArray;
    function AddObject: TJsonObject;
    procedure AddValue(AValue: TJsonValue);
    
    { 访问元素 }
    function GetString(Index: Integer; const DefaultValue: string = ''): string;
    function GetInteger(Index: Integer; DefaultValue: Integer = 0): Integer;
    function GetDouble(Index: Integer; DefaultValue: Double = 0.0): Double;
    function GetBoolean(Index: Integer; DefaultValue: Boolean = False): Boolean;
    
    { 操作 }
    procedure Clear;
    procedure Delete(Index: Integer);
    function IsEmpty: Boolean;
    
    { 序列化 }
    function ToJson: string;
    function ToPrettyJson(Indent: string = '  '; CurrentIndent: string = ''): string;
    
    property Count: Integer read GetCount;
    property Items[Index: Integer]: TJsonValue read GetItem; default;
  end;

  { JSON 对象类 }
  TJsonObject = class(TObject)
  private
    FKeys: TStringList;
    FValues: TList;
    function GetCount: Integer;
    function GetValue(const Key: string): TJsonValue;
    function GetKey(Index: Integer): string;
    function IndexOfKey(const Key: string): Integer;
  public
    constructor Create;
    destructor Destroy; override;
    
    { 添加/设置属性 }
    procedure PutNull(const Key: string);
    procedure PutString(const Key, AValue: string);
    procedure PutInteger(const Key: string; AValue: Integer);
    procedure PutInt64(const Key: string; AValue: Int64);
    procedure PutDouble(const Key: string; AValue: Double);
    procedure PutBoolean(const Key: string; AValue: Boolean);
    function PutArray(const Key: string): TJsonArray;
    function PutObject(const Key: string): TJsonObject;
    procedure PutValue(const Key: string; AValue: TJsonValue);
    
    { 获取值（带默认值）}
    function GetString(const Key: string; const DefaultValue: string = ''): string;
    function GetInteger(const Key: string; DefaultValue: Integer = 0): Integer;
    function GetInt64(const Key: string; DefaultValue: Int64 = 0): Int64;
    function GetDouble(const Key: string; DefaultValue: Double = 0.0): Double;
    function GetBoolean(const Key: string; DefaultValue: Boolean = False): Boolean;
    function GetArray(const Key: string): TJsonArray;
    function GetObject(const Key: string): TJsonObject;
    
    { 检查存在性 }
    function Has(const Key: string): Boolean;
    function HasString(const Key: string): Boolean;
    function HasNumber(const Key: string): Boolean;
    function HasBoolean(const Key: string): Boolean;
    function HasArray(const Key: string): Boolean;
    function HasObject(const Key: string): Boolean;
    
    { 操作 }
    procedure Remove(const Key: string);
    procedure Clear;
    function IsEmpty: Boolean;
    function GetKeys: TStringList;
    
    { 序列化 }
    function ToJson: string;
    function ToPrettyJson(Indent: string = '  '; CurrentIndent: string = ''): string;
    
    property Count: Integer read GetCount;
    property Values[const Key: string]: TJsonValue read GetValue;
    property KeyNames[Index: Integer]: string read GetKey;
  end;

{ 解析函数 }
function JsonParse(const JsonString: string): TJsonValue;
function JsonParseObject(const JsonString: string): TJsonObject;
function JsonParseArray(const JsonString: string): TJsonArray;

{ 验证函数 }
function IsValidJson(const JsonString: string): Boolean;

{ 转义函数 }
function JsonEscape(const S: string): string;
function JsonUnescape(const S: string): string;

{ 便捷构造函数 }
function JsonNull: TJsonValue;
function JsonString(const AValue: string): TJsonValue;
function JsonInteger(AValue: Integer): TJsonValue;
function JsonDouble(AValue: Double): TJsonValue;
function JsonBoolean(AValue: Boolean): TJsonValue;
function CreateJsonArray: TJsonArray;
function CreateJsonObject: TJsonObject;

implementation

{ 内部解析器 }
type
  TJsonParser = class(TObject)
  private
    FText: string;
    FPos: Integer;
    FLen: Integer;
    function Peek: Char;
    function Next: Char;
    procedure SkipWhitespace;
    function ParseValue: TJsonValue;
    function ParseStringValue: string;
    function ParseNumber: Double;
    function ParseArray: TJsonArray;
    function ParseObject: TJsonObject;
    function ParseBoolean: Boolean;
    function ParseNull: Boolean;
  public
    constructor Create(const AText: string);
    function Parse: TJsonValue;
  end;

{ TJsonParser }

constructor TJsonParser.Create(const AText: string);
begin
  inherited Create;
  FText := AText;
  FPos := 1;
  FLen := Length(AText);
end;

function TJsonParser.Peek: Char;
begin
  if FPos <= FLen then
    Result := FText[FPos]
  else
    Result := #0;
end;

function TJsonParser.Next: Char;
begin
  if FPos <= FLen then
  begin
    Result := FText[FPos];
    Inc(FPos);
  end
  else
    Result := #0;
end;

procedure TJsonParser.SkipWhitespace;
begin
  while (FPos <= FLen) and (FText[FPos] in [' ', #9, #10, #13]) do
    Inc(FPos);
end