from enum import IntEnum
from dataclasses import dataclass


class Action(IntEnum):
    READ = 3
    WRITE = 6


class RegisterEnum(IntEnum):
    robotMode = 258
    isPowerOnRobot = 260
    isSecurityStopped = 261
    isEmergencyStopped = 262
    isTeachButtonPressed = 263
    isPowerButtonPressed = 264
    isSafetySignalSuchThatWeShouldStop = 265
    safetyMode = 266
    # GeneralPurposeRegisters... generated from register_dict below
    register_128 = 128
    register_129 = 129
    register_130 = 130
    register_131 = 131
    register_132 = 132
    register_133 = 133
    register_134 = 134
    register_135 = 135
    register_136 = 136
    register_137 = 137
    register_138 = 138
    register_139 = 139
    register_140 = 140
    register_141 = 141
    register_142 = 142
    register_143 = 143
    register_144 = 144
    register_145 = 145
    register_146 = 146
    register_147 = 147
    register_148 = 148
    register_149 = 149
    register_150 = 150
    register_151 = 151
    register_152 = 152
    register_153 = 153
    register_154 = 154
    register_155 = 155
    register_156 = 156
    register_157 = 157
    register_158 = 158
    register_159 = 159
    register_160 = 160
    register_161 = 161
    register_162 = 162
    register_163 = 163
    register_164 = 164
    register_165 = 165
    register_166 = 166
    register_167 = 167
    register_168 = 168
    register_169 = 169
    register_170 = 170
    register_171 = 171
    register_172 = 172
    register_173 = 173
    register_174 = 174
    register_175 = 175
    register_176 = 176
    register_177 = 177
    register_178 = 178
    register_179 = 179
    register_180 = 180
    register_181 = 181
    register_182 = 182
    register_183 = 183
    register_184 = 184
    register_185 = 185
    register_186 = 186
    register_187 = 187
    register_188 = 188
    register_189 = 189
    register_190 = 190
    register_191 = 191
    register_192 = 192
    register_193 = 193
    register_194 = 194
    register_195 = 195
    register_196 = 196
    register_197 = 197
    register_198 = 198
    register_199 = 199
    register_200 = 200
    register_201 = 201
    register_202 = 202
    register_203 = 203
    register_204 = 204
    register_205 = 205
    register_206 = 206
    register_207 = 207
    register_208 = 208
    register_209 = 209
    register_210 = 210
    register_211 = 211
    register_212 = 212
    register_213 = 213
    register_214 = 214
    register_215 = 215
    register_216 = 216
    register_217 = 217
    register_218 = 218
    register_219 = 219
    register_220 = 220
    register_221 = 221
    register_222 = 222
    register_223 = 223
    register_224 = 224
    register_225 = 225
    register_226 = 226
    register_227 = 227
    register_228 = 228
    register_229 = 229
    register_230 = 230
    register_231 = 231
    register_232 = 232
    register_233 = 233
    register_234 = 234
    register_235 = 235
    register_236 = 236
    register_237 = 237
    register_238 = 238
    register_239 = 239
    register_240 = 240
    register_241 = 241
    register_242 = 242
    register_243 = 243
    register_244 = 244
    register_245 = 245
    register_246 = 246
    register_247 = 247
    register_248 = 248
    register_249 = 249
    register_250 = 250
    register_251 = 251
    register_252 = 252
    register_253 = 253
    register_254 = 254
    register_255 = 255
    register_666 = 666


#
# register_dict = {f"register_{i}": i for i in range(128, 255)}
#
# GeneralPurposeRegister = IntEnum("GeneralPurposeRegister", register_dict)  # pyright: ignore
#

@dataclass
class RegisterValue:
    register: RegisterEnum
    value: int
